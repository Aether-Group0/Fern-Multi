#!/bin/bash

if pgrep -x "anonsurf" > /dev/null
	then
	echo "[+] Anonsurf is active. Your traffic is being routed through Tor."
	else
		echo "[*] Anonsurf is not running. Starting it now..."
		sudo anonsurf start
		if [ $? -eq 0 ]; then
			echo "[+] Anonsurf started successfully."
		else
			echo "[!] Failed to start Anonsurf."
		fi
fi
