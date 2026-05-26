#!/bin/bash

# Check if anonsurf is currently running
if pgrep -x "anonsurf" > /dev/null
	then
	echo "Current Tor session detected. Rotating identity..."
	# Requesting a new circuit/IP
	sudo anonsurf change
	echo "Identity changed. You now have a new Tor exit node."
	else
		echo "Anonsurf is not running. Starting it now to establish a Tor connection..."
		sudo anonsurf start
		fi
