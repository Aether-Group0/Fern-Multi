#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_python(script_path, capture_output=False):
    script = os.path.join(BASE_DIR, script_path)
    if not os.path.exists(script):
        print(f"[!] Error: Script not found at {script}")
        return subprocess.run(["echo", ""], capture_output=capture_output, text=True)
    return subprocess.run(["python3", script], capture_output=capture_output, text=True)


def run_shell(script_path, capture_output=False):
    script = os.path.join(BASE_DIR, script_path)
    if not os.path.exists(script):
        print(f"[!] Error: Script not found at {script}")
        return subprocess.run(["echo", ""], capture_output=capture_output, text=True)
    return subprocess.run(["bash", script], capture_output=capture_output, text=True)


def clear_screen():
    os.system("clear")


def typewriter(text, speed=0.02):
    for char in str(text):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


def HTTP_SERV():
    run_python("HTTP_SERV/HTTP_SERV.py")
    input("\nPress Enter to return to menu...")
    Main_Menu()


def Port_FIND():
    result = run_shell("Tools-Other/Ip_Tools/port_FIND_using_Nmap.sh", capture_output=True)
    clear_screen()
    print(result.stdout)
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")


def SCAN_Through_TOR():
    result = run_shell("Tools-Other/Ip_Tools/TOR_SCANNER.sh", capture_output=True)
    clear_screen()
    print(result.stdout)
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")


def TV_DLP():
    result = run_shell("Tools-Other/MEDIA-MUNIPULATERS/TV-DLP.sh", capture_output=True)
    clear_screen()
    print(result.stdout)
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")


def NSlookup():
    run_python("Tools-Other/NSLOOKUP/NSlookupF.py")
    input("\nPress Enter to return to menu...")
    Main_Menu()


def Case77():
    run_python("Scripts/Case7793278432987.py")
    input("\nPress Enter to return to menu...")
    Main_Menu()


def RIp_ip():
    result = run_shell("Scripts/sha4665762I087pP97u798l87l.sh", capture_output=True)
    clear_screen()
    print(result.stdout)
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")


def GEOlocate():
    run_python("Scripts/GEO46587346398576326888888.py")
    input("\nPress Enter to return to menu...")
    Main_Menu()


def silent_Nmap_port_scan_ip():
    typewriter("Port Scan in progress...", speed=0.05)
    typewriter("...", speed=0.05)
    typewriter("...", speed=0.05)
    ip_var = input("enter ip you want to scan: ").strip()
    if not ip_var:
        print("[!] No IP provided.")
        return
    subprocess.run(["nmap", ip_var, "-sS"])

    menu = input("press M to go to main menu: ").strip().lower()
    if menu == "m":
        Main_Menu()
    else:
        print("[!] Not valid command")


def os_Nmap_scan():
    typewriter("OS Scan in progress...", speed=0.05)
    typewriter("...", speed=0.05)
    typewriter("...", speed=0.05)
    ip_var = input("enter ip you want to scan: ").strip()
    if not ip_var:
        print("[!] No IP provided.")
        return
    result = subprocess.run(["nmap", ip_var, "-O"], capture_output=True, text=True)
    typewriter(result.stdout, speed=0.005)

    menu = input("press M to go to main menu: ").strip().lower()
    if menu == "m":
        Main_Menu()
    else:
        print("[!] Not valid command")


def msfvenom_payload_generater():
    result = run_shell("Scripts/PayTime.sh", capture_output=True)
    clear_screen()
    print(result.stdout)
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")

    menu = input("press M to go to main menu: ").strip().lower()
    if menu == "m":
        Main_Menu()
    else:
        print("[!] Not valid command")


def splash_screen():
    print("\n=== FERN MULTI ===")


def Help():
    splash_screen()
    print("\nFern Multi Help\n------------")
    print("Fern SNp: Silent Nmap Scan")
    print("Fern OSN: Nmap OS Scan")
    print("Fern PayTime: Payload Generator")
    print("Fern Rip-PH: IP/Phone Data Tool")
    print("Fern GEO: Geolocate IP Addresses")
    print("Fern CASE: Execute Case77 Script")
    print("Fern HTTP: Start Local HTTP Server")
    print("Fern TOR-S: Network Scan through TOR")
    print("Fern TV-DLP: Media Manipulation Tool")
    print("Fern NSlookup: DNS Lookup Tool")
    print("Fern-h: Help Menu")
    input("\nPress Enter to return to menu...")
    Main_Menu()


def Main_Menu():
    splash_screen()
    choice = input("Type Fern before: ").strip()

    if choice == "Fern SNp":
        silent_Nmap_port_scan_ip()
    elif choice == "Fern OSN":
        os_Nmap_scan()
    elif choice == "Fern PayTime":
        msfvenom_payload_generater()
    elif choice == "Fern Rip-PH":
        RIp_ip()
    elif choice == "Fern GEO":
        GEOlocate()
    elif choice == "Fern CASE":
        Case77()
    elif choice == "Fern HTTP":
        HTTP_SERV()
    elif choice == "Fern TOR-S":
        SCAN_Through_TOR()
    elif choice == "Fern TV-DLP":
        TV_DLP()
    elif choice == "Fern NSlookup":
        NSlookup()
    elif choice == "Fern-h":
        Help()
    else:
        print("[!] Invalid Command")


if __name__ == "__main__":
    Main_Menu()
