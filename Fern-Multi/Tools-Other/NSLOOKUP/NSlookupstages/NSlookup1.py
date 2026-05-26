import subprocess


def nslookup_domain(domain):
    try:
        result = subprocess.run(['nslookup', domain], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except Exception as e:
        print("An error occurred:", e)


def main():
    domain = input("Enter a domain to lookup: ").strip()
    confirm = input(f"You entered '{domain}'. Confirm? (y/n): ").strip().lower()
    if confirm == 'y':
        nslookup_domain(domain)
    else:
        print("Domain lookup canceled.")

if __name__ == '__main__':
    main()