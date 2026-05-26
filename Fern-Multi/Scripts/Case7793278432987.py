import os
import subprocess
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

def enable_ip_forwarding():
    """Enable IP forwarding on the system."""
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            f.write('1')
        print("IP forwarding enabled.")
    except PermissionError:
        print("Permission denied: Run this script as root.")
        exit(1)

def configure_iptables():
    """Set up NAT using iptables."""
    try:

        subprocess.run(['iptables', '-F'], check=True)
        subprocess.run(['iptables', '-t', 'nat', '-F'], check=True)

        subprocess.run(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'eth0', '-j', 'MASQUERADE'], check=True)
        subprocess.run(['iptables', '-A', 'FORWARD', '-i', 'eth0', '-o', 'eth0', '-j', 'ACCEPT'], check=True)

        print("iptables rules configured.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring iptables: {e}")
        exit(1)

def log_traffic():
    """Log network traffic to a JSON file with timestamps."""
    log_dir = "json logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "network_traffic_log.json")
    try:
        with open(log_file, 'a') as f:
            while True:
                # replace with actual traffic capture logic
                traffic_data = {
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
                    "source": "192.168.1.1",
                    "destination": "192.168.1.2",
                    "protocol": "TCP",
                    "data": "Example traffic data"
                }
                json.dump(traffic_data, f)
                f.write('\n')
                time.sleep(1)  
    except KeyboardInterrupt:
        print("Traffic logging stopped.")

def start_http_server():
    """Start an HTTP server to handle requests and redirect to login page for specific domains."""
    log_dir = "json logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "http_requests_log.json")

    class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            client_ip = self.client_address[0]
            print(f"Received GET request from {client_ip}")
           
            if "https://www.google.com/" in self.path:
        
                self.send_response(302)
                self.send_header("Location", "/login")
                self.end_headers()

                request_data = {
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
                    "client_ip": client_ip,
                    "method": "GET",
                    "path": self.path,
                    "action": "redirected to login"
                }
                with open(log_file, 'a') as log_f:
                    json.dump(request_data, log_f)
                    log_f.write('\n')
                return

            html_folder = "Case77 Assets"
            html_file = os.path.join(html_folder, "login.html")

            if os.path.exists(html_file):
                with open(html_file, 'r') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))

                request_data = {
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
                    "client_ip": client_ip,
                    "method": "GET",
                    "path": self.path
                }
                with open(log_file, 'a') as log_f:
                    json.dump(request_data, log_f)
                    log_f.write('\n')
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    server_address = ("", 8080)  # Listen on all interfaces, port 8080
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    print("HTTP server running on port 8080...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("HTTP server stopped.")

def main():
    print("Setting up the computer as a network gateway...")
    enable_ip_forwarding()
    configure_iptables()
    print("Starting traffic logging...")
    log_traffic()
    print("Starting HTTP server...")
    start_http_server()

if __name__ == "__main__":
    main()