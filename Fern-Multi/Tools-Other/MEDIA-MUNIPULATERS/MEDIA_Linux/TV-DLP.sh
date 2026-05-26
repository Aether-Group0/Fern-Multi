#!/bin/bash

# --- CONFIGURATION ---
VIDEO_DIR="$HOME/Downloads/Videos"
AUDIO_DIR="$HOME/Downloads/Audio"

# --- ASCII LOGO ---
clear
echo "====================================================="
echo "  __     _______     ____  _     ____  "
echo "  \ \   / /_   _|   |  _ \| |   |  _ \ "
echo "   \ \ / /  | |_____| | | | |   | |_) |"
echo "    \ V /   | |_____| |_| | |___|  __/ "
echo "     \_/    |_|     |____/|_____|_|    "
echo "           MEDIA DOWNLOADER v2.0"
echo "====================================================="

if ! command -v yt-dlp &> /dev/null; then
	echo -e "\n[!] Error: yt-dlp is not installed."
	exit 1
	fi
	
	echo -e "\n"
	read -p "Enter URL (Video or Playlist): " URL
	if [ -z "$URL" ]; then echo "No URL provided. Exiting."; exit 1; fi
		
		echo -e "\nSELECT FORMAT:"
		echo "1) Video (Best Quality MP4)"
		echo "2) Audio Only (High Quality MP3)"
		read -p "Selection [1-2]: " CHOICE
		
		echo -e "\nPLAYLIST SETTINGS:"
		echo "1) Download entire playlist (into a sub-folder)"
		echo "2) Download single item only"
		read -p "Selection [1-2]: " PL_CHOICE
		
		if [ "$PL_CHOICE" == "1" ]; then
			PL_FLAGS="--yes-playlist --output %(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"
			else
				PL_FLAGS="--no-playlist --output %(title)s.%(ext)s"
				fi
				
				# CHANGED TO FIREFOX HERE
				COOKIE_FLAG="--cookies-from-browser firefox"
				
				case $CHOICE in
				1)
				mkdir -p "$VIDEO_DIR"
				cd "$VIDEO_DIR" || exit
				echo -e "\n[+] Downloading Video to: $VIDEO_DIR"
				yt-dlp -f "bestvideo+bestaudio/best" \
				--merge-output-format mp4 \
				$COOKIE_FLAG \
				$PL_FLAGS \
				"$URL"
				;;
				2)
				mkdir -p "$AUDIO_DIR"
				cd "$AUDIO_DIR" || exit
				echo -e "\n[+] Downloading Audio to: $AUDIO_DIR"
				yt-dlp -x --audio-format mp3 \
				--audio-quality 0 \
				$COOKIE_FLAG \
				$PL_FLAGS \
				"$URL"
				;;
				*)
				echo "Invalid option. Exiting."
				exit 1
				;;
				esac
				
				echo -e "\n====================================================="
				echo "DONE! Files are located in: $(pwd)"
				echo "====================================================="
