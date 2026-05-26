import subprocess
import sys

def reverse_lookup(ip_address):
    """Perform reverse DNS lookup on an IP address"""
    print(f"\n=== Reverse Lookup for {ip_address} ===\n")
    
    try:
        
        result = subprocess.run(
            ['nslookup', ip_address],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print(result.stdout)
        
        if result.stderr:
            print(f"Error: {result.stderr}")
    
    except subprocess.TimeoutExpired:
        print(f"Error: Lookup timed out for {ip_address}")
    except Exception as e:
        print(f"Error: {e}")

def validate_ip(ip_address):
    """Basic IP validation"""
    parts = ip_address.split('.')
    
    if len(parts) != 4:
        return False
    
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    
    return True


if __name__ == "__main__":
    ip = input("Enter IP address to lookup: ").strip()
    
    if not validate_ip(ip):
        print(f"Error: '{ip}' is not a valid IP address")
        sys.exit(1)
    
    reverse_lookup(ip)