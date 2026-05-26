GET_IP(){

    read -p "Enter Target IP: " IP
}

GET_IP

nmap -sV "$IP"