import sys
import argparse
import requests
import ipaddress


class Config:
    """Configuration class for color codes and messages"""
    COLORS = {
        'lblue': '\033[96m',
        'red': '\033[91m',
        'grn': '\033[32m',
        'ylw': '\033[93m',
        'reset': '\033[0m'
    }

    @property
    def banner(self):
        """Returns a stylized banner for the application."""
        return f"""
{self.COLORS['lblue']}╔════════════════════════════════════════════════════════╗
{self.COLORS['lblue']}║                                                        ║
{self.COLORS['lblue']}║   {self.COLORS['red']}██╗  ██████╗      {self.COLORS['grn']}IP Location Finder                 {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██╔══██╗     {self.COLORS['grn']}Secure API Edition                 {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██████╔╝     {self.COLORS['grn']}Powered by {self.COLORS['ylw']}ipinfo.io             {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██╔═══╝      {self.COLORS['ylw']}Version {self.COLORS['red']}2.0                    {self.COLORS['lblue']}    ║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██║                                  {self.COLORS['lblue']}           ║
{self.COLORS['lblue']}║   {self.COLORS['red']}╚═╝  ╚═╝                                  {self.COLORS['lblue']}           ║
{self.COLORS['lblue']}║                                                        ║
{self.COLORS['lblue']}╚════════════════════════════════════════════════════════╝
{self.COLORS['reset']}"""


class IPLocator:
    """Handles secure IP location data retrieval"""
    # Upgraded to a secure HTTPS endpoint
    API_URL = 'https://ipinfo.io/{}/json'

    def __init__(self, ip):
        self.ip = ip

    def get_data(self):
        """Fetch and validate IP data from API securely"""
        try:
            # Adding a standard User-Agent prevents some basic API blocks
            headers = {'User-Agent': 'IPLocator-CLI/2.0'}
            response = requests.get(self.API_URL.format(self.ip), headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Handle specific API error responses
            if 'error' in data:
                raise ValueError(f"API Error: {data['error'].get('message', 'Unknown error')}")

            return data
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Secure connection failed: {str(e)}") from e


class OutputFormatter:
    """Handles output formatting and display"""
    def __init__(self, config):
        self.colors = config.COLORS
        self.banner = config.banner

    def show_banner(self):
        print(self.banner)

    def display_results(self, data):
        """Display formatted results mapped to the ipinfo API"""
        
        # ipinfo.io combines lat/lon into a single 'loc' string
        lat, lon = "N/A", "N/A"
        if 'loc' in data:
            lat_lon = data['loc'].split(',')
            if len(lat_lon) == 2:
                lat, lon = lat_lon[0], lat_lon[1]

        fields = [
            ('IP', data.get('ip', 'N/A')),
            ('COUNTRY CODE', data.get('country', 'N/A')),
            ('REGION', data.get('region', 'N/A')),
            ('CITY', data.get('city', 'N/A')),
            ('ZIP/POSTAL', data.get('postal', 'N/A')),
            ('LATITUDE', lat),
            ('LONGITUDE', lon),
            ('TIME ZONE', data.get('timezone', 'N/A')),
            ('ORG / ISP', data.get('org', 'N/A')), # ipinfo combines ISP and ASN into 'org'
        ]

        # Upgraded to a functioning, secure Google Maps link
        google_map = f"https://www.google.com/maps?q={lat},{lon}" if lat != "N/A" else "N/A"

        print(f"\n{self.colors['grn']}{' SECURE IP LOCATION INFORMATION ':-^60}{self.colors['reset']}\n")
        for display_name, value in fields:
            print(f"    {self.colors['grn']}[{self.colors['red']}+{self.colors['grn']}] {self.colors['lblue']}{display_name:<12} {self.colors['red']}::: {self.colors['ylw']}{value}")

        print(f"\n    {self.colors['grn']}[{self.colors['red']}+{self.colors['grn']}] {self.colors['lblue']}GOOGLE MAP   {self.colors['red']}::: {self.colors['ylw']}{google_map}")
        print(f"\n{self.colors['grn']}{'-' * 60}{self.colors['reset']}\n")


def validate_ip(ip):
    """Validate IP format and ensure it's not a private/internal IP"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback:
            return False, "Cannot geolocate private or local loopback IPs (e.g., 192.168.x.x or 127.0.0.1)."
        return True, ""
    except ValueError:
        return False, "Invalid IP address format."


def main():
    config = Config()
    formatter = OutputFormatter(config)
    formatter.show_banner()

    # Using argparse makes the script robust against bad user input
    parser = argparse.ArgumentParser(
        description=f"{config.COLORS['grn']}IP Location Finder CLI{config.COLORS['reset']}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('-I', '--ip', dest='ip_address', required=True, 
                        help='Get secure geolocation information for a specific IP')

    # If no arguments are provided, show help and exit cleanly
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Run the upgraded safety checks
    is_valid, error_msg = validate_ip(args.ip_address)
    if not is_valid:
        print(f"\n{config.COLORS['red']}Error: {error_msg}{config.COLORS['reset']}")
        sys.exit(1)

    # Execute the API call
    try:
        locator = IPLocator(args.ip_address)
        data = locator.get_data()
        formatter.display_results(data)
    except Exception as e:
        print(f"\n{config.COLORS['red']}Error: {str(e)}{config.COLORS['reset']}")


if __name__ == "__main__":
    main()