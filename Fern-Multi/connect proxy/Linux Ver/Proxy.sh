if pgrep -x "anonsurf" > /dev/null
	then
	echo "Anonsurf is active. Your traffic is being routed through Tor."
	else
		echo "Anonsurf is not running. Starting it now..."
		sudo anonsurf start
		fi
		
