#!/usr/bin/env python3
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))


def run_tool(script_path):
    full_path = os.path.join(ROOT_DIR, script_path)
    return subprocess.run(["python3", full_path], text=True)


def Exit():
    print("Exiting...")
    run_tool("Fern-Multi-tool.py")
    sys.exit()


def Logic(user_input):
    if user_input == "Look":
        NSLOOKUP()
    elif user_input == "Rev":
        Rev()
    elif user_input == "Exit":
        Exit()
    else:
        print("\n[!] Command not Recognized. Please try again.")


def Rev():
    subprocess.run(["python3", os.path.join(BASE_DIR, "NSlookupstages", "REV.py")], text=True)


def NSLOOKUP():
    subprocess.run(["python3", os.path.join(BASE_DIR, "NSlookupstages", "NSlookup1.py")], text=True)


def Get_User_Input():
    return input("\nChoose action: ").strip()


def Main_Menu():
    while True:
        print("\n--- Main Menu ---")
        print("Domain_Lookup")
        print("reverse Domain_Lookup")
        print("Exit")
        print("To choose Domain_lookup type 'Look', to choose reverse type 'Rev'.")

        choice = Get_User_Input()
        Logic(choice)


if __name__ == "__main__":
    Main_Menu()
