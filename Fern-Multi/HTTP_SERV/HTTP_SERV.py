import http.server
import socketserver
import os
import socket
import shutil
import ssl

BASE_DESTINATION = "HTTP SERVERS"
source_path = input("Enter folder path to copy and host: ").strip().replace('"', '').replace("'", "")

if not os.path.isdir(source_path):
    print(f"Error: folder '{source_path}' not found.")
    exit()

if not os.path.exists(BASE_DESTINATION):
    os.makedirs(BASE_DESTINATION)

folder_name = os.path.basename(source_path.rstrip(os.sep))
final_destination = os.path.join(BASE_DESTINATION, folder_name)

try:
    if os.path.exists(final_destination):
        shutil.rmtree(final_destination)
    shutil.copytree(source_path, final_destination)
except Exception as e:
    print(f"Copy failed: {e}")
    exit()

PORT = 443
CERT_FILE = "server.pem"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=final_destination, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    try:
        context.load_cert_chain(certfile=CERT_FILE)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"https://{local_ip}:{PORT}")
        
        httpd.serve_forever()
        
    except FileNotFoundError:
        print(f"Error: '{CERT_FILE}' not found.")
    except PermissionError:
        print(f"Error: Permission denied on port {PORT}.")
    except KeyboardInterrupt:
        print("\nStopped.")