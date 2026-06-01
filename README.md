# Fern-Multi

!Warning! Fern-Multi is meant mainly for Linux systems. We are working on a Windows version.
Fern-Multi is a powerful tool that combines several scripts for network scanning, DNS lookups, and local HTTP serving.

## Installation

Run the installer from the repository root:

```bash
bash install.sh
```

## Usage

Start the main menu with:

```bash
python3 Fern-Multi/Fern-Multi-tool.py
```

## Requirements

### System-Level Tools/Executables

- `python3` - Core requirement for running Python scripts
- `bash` - Shell scripting execution
- `nmap` - Network port scanning and OS detection
- `msfvenom` - Metasploit payload generation
- `msf framework` - Metasploit Framework backend
- `git` - Version control (for installation)
- `curl` - HTTP requests (used in scripts)
- `tshark` (Wireshark) - Network traffic analysis and packet capture
- `tor` - TOR network connectivity (for proxy/anonymity features)

### Python Libraries (Standard Library)

- `os` - Operating system interactions
- `subprocess` - Process execution
- `sys` - System-specific parameters
- `time` - Time delays and timing
- `random` - Random number generation
- `json` - JSON data handling
- `argparse` - Command-line argument parsing
- `http.server` - HTTP server functionality
- `socketserver` - Socket server handling
- `socket` - Network socket operations
- `shutil` - File operations
- `ssl` - SSL/TLS encryption
- `ipaddress` - IP address validation
- `pathlib` - File path handling
- `datetime` - Date/time operations

### Python Libraries (Third-Party - External Packages)

- `requests` - HTTP requests (for GEO location lookup)
- `httpx` - Async HTTP client (for GGUF model downloads)
- `llm` - Language model framework (for GGUF runner)
- `llama_cpp` - Python bindings for llama.cpp (local LLM inference)
- `click` - CLI command framework (for GGUF runner)
