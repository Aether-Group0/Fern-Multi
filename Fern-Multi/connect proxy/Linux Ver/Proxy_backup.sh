#!/bin/bash

if pgrep -x "anonsurf" > /dev/null
	then
	echo "You are connected to TOR meaning all of your internet traffic will go through TOR meaning you are anonymous"
	
	else
		anonsurf start
fi
