@echo off
REM TOR Scanner - Windows Batch version

setlocal enabledelayedexpansion

set "TOR_PROXY=socks4://127.0.0.1:9050"

:RUN_TOR_SCAN
cls
echo ======================================
echo            TOR-SCANNER               
echo ======================================
echo.

set /p TARGET="[+] Enter Target IP or Domain: "

if "!TARGET!"=="" (
    echo [!] Error: No target specified.
    echo.
    pause
    goto RUN_TOR_SCAN
)

echo [*] Initializing scan through Tor...
echo [*] Proxy: !TOR_PROXY!
echo [*] Scanning !TARGET!...
echo.

nmap -Pn -sT --proxies "!TOR_PROXY!" -F "!TARGET!"

pause
goto RUN_TOR_SCAN
