#!/usr/bin/env python3
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FERN_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))


def tor_script(script_name):
    script_path = os.path.join(FERN_DIR, "connect proxy", script_name)
    return subprocess.run(["bash", script_path], capture_output=True, text=True)


def clear_screen():
    subprocess.run(["clear"])


def Change_TOR_ID():
    result = tor_script("Change_ID_Proxy.sh")
    clear_screen()
    print(result.stdout)


def Connect_To_TOR():
    result = tor_script("Proxy.sh")
    clear_screen()
    print(result.stdout)


def Disconnect_From_TOR():
    result = tor_script("end_proxy.sh")
    clear_screen()
    print(result.stdout)


def main_menu():
    while True:
        choice = input("Enter Connect, Disconnect, Change ID, or Exit: ").strip().lower()
        if choice in ("connect", "connect to the tor network"):
            Connect_To_TOR()
        elif choice in ("disconnect", "disconnect from the tor network"):
            Disconnect_From_TOR()
        elif choice in ("change id", "change your id on the tor network", "change"):
            Change_TOR_ID()
        elif choice in ("exit", "quit"):
            break
        else:
            print("[!] Command not recognized. Please try again.")

    print("Returning to Fern Multi menu.")
    subprocess.run(["python3", os.path.join(FERN_DIR, "Fern-Multi-tool.py")])


if __name__ == "__main__":
    main_menu()
