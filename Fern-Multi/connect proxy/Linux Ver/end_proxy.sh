#!/bin/bash

# 1. Attempt to stop the service
sudo anonsurf stop

# 2. Check if it's still hanging around
if pgrep -x "anonsurf" > /dev/null
	then
	echo "Anonsurf is being stubborn. Force-stopping again..."
	sudo anonsurf stop
	else
		echo "Anonsurf has stopped. Your traffic is no longer routed through Tor."
		fi
