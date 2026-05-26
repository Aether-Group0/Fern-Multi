@echo off
REM Port finder using Nmap - Windows Batch version

setlocal enabledelayedexpansion

:GET_IP
set /p IP="Enter Target IP: "

if "!IP!"=="" (
    echo [!] Error: No IP specified.
    goto GET_IP
)

echo.
echo Starting Nmap scan on !IP!...
echo.

nmap -sV "!IP!"

pause
