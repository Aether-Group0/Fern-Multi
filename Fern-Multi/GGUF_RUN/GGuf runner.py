import click
import httpx
import json
import llm
import pathlib
import sys
import datetime
from llama_cpp import Llama, llama_chat_format

# --- Model Catalog (HuggingFace GGUF Links) ---
# These are pre-selected high-performance models for 2026
MODEL_CATALOG = {
    "llama3-8b": {
        "url": "https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
        "aliases": ["llama3", "llama"],
        "description": "Meta's flagship 8B model. Best for general reasoning."
    },
    "phi3-mini": {
        "url": "https://huggingface.co/bartowski/Phi-3-mini-4k-instruct-GGUF/resolve/main/Phi-3-mini-4k-instruct-Q4_K_M.gguf",
        "aliases": ["phi3", "phi"],
        "description": "Microsoft's lightweight 3.8B model. Very fast on CPUs."
    },
    "mistral-7b": {
        "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "aliases": ["mistral"],
        "description": "The reliable industry standard for instructions."
    },
    "qwen2.5-1.5b": {
        "url": "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "aliases": ["qwen", "tiny"],
        "description": "Ultra-small, ultra-fast. Perfect for low-end hardware."
    }
}

# --- Directory & Persistence Helpers ---

def _get_gguf_dir():
    directory = llm.user_dir() / "gguf"
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def _ensure_models_dir():
    directory = _get_gguf_dir() / "models"
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def _ensure_logs_dir():
    directory = _get_gguf_dir() / "logs"
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def _get_config_file(filename):
    filepath = _get_gguf_dir() / filename
    if not filepath.exists():
        filepath.write_text("{}")
    return filepath

def human_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0: break
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} {unit}"

# --- Settings Management ---

def load_settings():
    path = _get_config_file("settings.json")
    defaults = {"default_n_ctx": 2048, "n_gpu_layers": 0}
    data = json.loads(path.read_text())
    return {**defaults, **data}

def save_settings(settings):
    path = _get_config_file("settings.json")
    path.write_text(json.dumps(settings, indent=2))

# --- Plugin Registration Hooks ---

@llm.hookimpl
def register_models(register):
    models_file = _get_config_file("models.json")
    models = json.loads(models_file.read_text())
    for model_id, info in models.items():
        register(
            GgufChatModel(
                model_id,
                info["path"],
                n_ctx=info.get("n_ctx", 0),
            ),
            aliases=info.get("aliases", [])
        )

@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def gguf():
        "Advanced GGUF Model Management"

    @gguf.command()
    @click.option("--n-ctx", type=int, help="Default context window (e.g. 4096)")
    @click.option("--gpu", type=int, help="GPU Layers to offload (-1 for all)")
    def setup(n_ctx, gpu):
        "Configure global hardware and performance settings"
        settings = load_settings()
        if n_ctx: settings["default_n_ctx"] = n_ctx
        if gpu is not None: settings["n_gpu_layers"] = gpu
        save_settings(settings)
        click.secho(f"Settings saved to {_get_config_file('settings.json')}", fg="green")

    @gguf.command()
    def catalog():
        "List high-performance models available for download"
        click.secho("\n--- Available HuggingFace Catalog ---", fg="green", bold=True)
        for name, d in MODEL_CATALOG.items():
            click.secho(f"\n{name} (Aliases: {', '.join(d['aliases'])})", fg="cyan", bold=True)
            click.echo(f"  {d['description']}")

    @gguf.command()
    @click.argument("name")
    def install(name):
        "Download and auto-register a model from the catalog"
        if name not in MODEL_CATALOG:
            raise click.ClickException(f"Model '{name}' not found in catalog. Run 'llm gguf catalog'.")
        
        info = MODEL_CATALOG[name]
        download_path = _ensure_models_dir() / info["url"].split("/")[-1]
        
        if not download_path.exists():
            click.echo(f"Requesting {name}...")
            with httpx.stream("GET", info["url"], follow_redirects=True) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                with click.progressbar(length=total, label=f"Downloading {human_size(total)}") as bar:
                    with open(download_path, "wb") as f:
                        for chunk in r.iter_bytes(1024):
                            f.write(chunk)
                            bar.update(len(chunk))
        
        models = json.loads(_get_config_file("models.json").read_text())
        models[name] = {"path": str(download_path.resolve()), "aliases": info["aliases"]}
        _get_config_file("models.json").write_text(json.dumps(models, indent=2))
        click.secho(f"\nSuccessfully installed and registered {name}!", fg="green")

    @gguf.command()
    @click.argument("model_id")
    def uninstall(model_id):
        "Remove a model registration and delete its .gguf file"
        models_file = _get_config_file("models.json")
        models = json.loads(models_file.read_text())
        if model_id in models:
            path = pathlib.Path(models[model_id]["path"])
            if path.exists():
                path.unlink()
                click.secho(f"Deleted file: {path.name}", fg="yellow")
            del models[model_id]
            models_file.write_text(json.dumps(models, indent=2))
            click.secho(f"Unregistered {model_id} from database.", fg="green")
        else:
            click.echo("Model not found in registry.")

    @gguf.command()
    @click.argument("id_or_alias")
    @click.option("--system", default="You are a helpful AI assistant.", help="The AI Persona")
    def chat(id_or_alias, system):
        "Interactive Terminal Chat with Auto-Logging"
        models = json.loads(_get_config_file("models.json").read_text())
        info = models.get(id_or_alias) or next((m for m in models.values() if id_or_alias in m.get("aliases", [])), None)
        
        if not info: raise click.ClickException(f"No registered model matches '{id_or_alias}'.")

        click.echo(f"Loading {id_or_alias}...")
        model_instance = GgufChatModel(id_or_alias, info["path"])
        llm_obj = model_instance.get_model()
        
        messages = [{"role": "system", "content": system}]
        click.secho("\nChat Session Started. Type 'exit' to end session.", fg="green", bold=True)
        
        try:
            while True:
                user_input = click.prompt(click.style("You", fg="blue", bold=True))
                if user_input.lower() in ("exit", "quit"): break
                
                messages.append({"role": "user", "content": user_input})
                click.secho("AI: ", fg="cyan", bold=True, nl=False)
                
                response_text = ""
                completion = llm_obj.create_chat_completion(messages=messages, stream=True)
                for chunk in completion:
                    content = chunk["choices"][0].get("delta", {}).get("content", "")
                    click.echo(content, nl=False)
                    response_text += content
                
                click.echo("\n")
                messages.append({"role": "assistant", "content": response_text})
        finally:
            log_path = _ensure_logs_dir() / f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            log_path.write_text(json.dumps(messages, indent=2))
            click.secho(f"\nSession saved to {log_path}", fg="dim")

# --- Logic Classes ---

class GgufChatModel(llm.Model):
    model_id = "gguf"
    can_stream = True

    def __init__(self, model_id, model_path, n_ctx=0):
        self.model_id = f"gguf/{model_id}"
        self.model_path = model_path
        settings = load_settings()
        self.n_ctx = n_ctx or settings["default_n_ctx"]
        self.gpu = settings["n_gpu_layers"]
        self._model = None

    def get_model(self):
        if self._model is None:
            self._model = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_gpu_layers=self.gpu,
                verbose=False
            )
        return self._model

    def execute(self, prompt, stream, response, conversation):
        """Execute the model following llm.Model signature"""
        model = self.get_model()
        messages = []
        
        # Build conversation history
        if conversation:
            for prev in conversation.responses:
                messages.append({"role": "user", "content": prev.prompt.prompt})
                messages.append({"role": "assistant", "content": prev.text()})
        
        # Add system prompt if present
        if prompt.system:
            messages.insert(0, {"role": "system", "content": prompt.system})
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt.prompt})

        # Execute with stream or non-stream
        completion = model.create_chat_completion(messages=messages, stream=stream)
        
        if stream:
            for chunk in completion:
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                if content:
                    yield content
        else:
            # For non-streaming, yield the complete response
            yield completion["choices"][0]["message"]["content"]
