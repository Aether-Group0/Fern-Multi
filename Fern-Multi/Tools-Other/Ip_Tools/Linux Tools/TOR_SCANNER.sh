

TOR_PROXY="socks4://127.0.0.1:9050"

RUN_TOR_SCAN() {
    echo "======================================"
    echo "            TOR-SCANNER               "
    echo "======================================"
    
    read -p "[+] Enter Target IP or Domain: " TARGET

   
    if [[ -z "$TARGET" ]]; then
        echo "[!] Error: No target specified."
        return
    fi

    echo "[*] Initializing scan through Tor..."
    echo "[*] Proxy: $TOR_PROXY"
    echo "[*] Scanning $TARGET..."

    nmap -Pn -sT --proxies "$TOR_PROXY" -F "$TARGET"
}

n
RUN_TOR_SCAN