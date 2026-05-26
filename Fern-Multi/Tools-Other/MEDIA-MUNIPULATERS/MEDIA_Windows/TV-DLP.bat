@echo off
REM TV-DLP Media Downloader - Windows Batch version

setlocal enabledelayedexpansion

REM --- CONFIGURATION ---
set "VIDEO_DIR=%USERPROFILE%\Downloads\Videos"
set "AUDIO_DIR=%USERPROFILE%\Downloads\Audio"

REM --- ASCII LOGO ---
cls
echo =====================================================
echo   __     _______     ____  _     ____  
echo   \ \   / /_   _^|   ^|  _ \^| ^|   ^|  _ \ 
echo    \ \ / /  ^| ^|_____^| ^| ^| ^| ^|   ^| ^|_) ^)
echo     \ V /   ^| ^|_____^| ^|_^| ^| ^|___^|  __/ 
echo      \_/    ^|_^|     ^|____/^|_____|_^|    
echo            MEDIA DOWNLOADER v2.0
echo =====================================================

REM Check if yt-dlp is installed
where yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Error: yt-dlp is not installed.
    echo [*] Install it with: pip install yt-dlp
    pause
    exit /b 1
)

echo.
set /p URL="Enter URL (Video or Playlist): "
if "!URL!"=="" (
    echo No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo SELECT FORMAT:
echo 1) Video (Best Quality MP4)
echo 2) Audio Only (High Quality MP3)
set /p CHOICE="Selection [1-2]: "

echo.
echo PLAYLIST SETTINGS:
echo 1) Download entire playlist (into a sub-folder)
echo 2) Download single item only
set /p PL_CHOICE="Selection [1-2]: "

if "!PL_CHOICE!"=="1" (
    set "PL_FLAGS=--yes-playlist --output %(playlist_title)s\%(playlist_index)s-%(title)s.%(ext)s"
) else (
    set "PL_FLAGS=--no-playlist --output %(title)s.%(ext)s"
)

REM Using Firefox for cookies
set "COOKIE_FLAG=--cookies-from-browser firefox"

if "!CHOICE!"=="1" (
    if not exist "!VIDEO_DIR!" mkdir "!VIDEO_DIR!"
    cd /d "!VIDEO_DIR!" || exit /b 1
    echo.
    echo [+] Downloading Video to: !VIDEO_DIR!
    echo.
    yt-dlp -f "bestvideo+bestaudio/best" ^
    --merge-output-format mp4 ^
    !COOKIE_FLAG! ^
    !PL_FLAGS! ^
    "!URL!"
) else if "!CHOICE!"=="2" (
    if not exist "!AUDIO_DIR!" mkdir "!AUDIO_DIR!"
    cd /d "!AUDIO_DIR!" || exit /b 1
    echo.
    echo [+] Downloading Audio to: !AUDIO_DIR!
    echo.
    yt-dlp -x --audio-format mp3 ^
    --audio-quality 0 ^
    !COOKIE_FLAG! ^
    !PL_FLAGS! ^
    "!URL!"
) else (
    echo Invalid option. Exiting.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo DONE! Files are located in: !CD!
echo =====================================================
pause
