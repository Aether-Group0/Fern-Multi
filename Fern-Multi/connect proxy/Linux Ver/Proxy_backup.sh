if pgrep -x "anonsurf" > /dev/null
	then
	print("You are connected to TOR meaning all of your internet traffic will go through TOR meaning you are annonymous")
	
	else
		anonsurf start
