import socket
import ipaddress
import threading
from concurrent.futures import ThreadPoolExecutor
import os

def get_local_network():
    """Identify the local network IP range."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet = local_ip.rsplit('.', 1)[0] + '.0/24'
    print(f"Local IP: {local_ip}")
    print(f"Scanning network: {subnet}")
    return subnet

def ping_host(ip):
    """Ping a host to check if it's alive."""
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1" if os.name != "nt" else f"ping -n 1 -w 1 {ip} > nul")
    return response == 0

def scan_port(host, port):
    """Scans a single port on a host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                return port
    except Exception:
        pass
    return None

def scan_ports_on_host(host, start_port=1, end_port=1024):
    """Scan a range of ports on a given host."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: scan_port(host, p), range(start_port, end_port + 1))
    for port in results:
        if port:
            open_ports.append(port)
    return open_ports

def network_scan(subnet, start_port=1, end_port=1024):
    """Discover devices on the network and scan open ports on each."""
    alive_hosts = []
    open_ports_map = {}
    print("Discovering devices on the network...")
    
    # Discover devices
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping_host, (str(ip) for ip in ipaddress.IPv4Network(subnet, strict=False)))
    for ip, is_alive in zip(ipaddress.IPv4Network(subnet, strict=False), results):
        if is_alive:
            alive_hosts.append(str(ip))
    
    print(f"Alive hosts: {alive_hosts}")
    
    # Scan ports on each discovered host
    for host in alive_hosts:
        print(f"Scanning ports on {host}...")
        open_ports = scan_ports_on_host(host, start_port, end_port)
        if open_ports:
            open_ports_map[host] = open_ports
    
    return open_ports_map

if __name__ == "__main__":
    subnet = get_local_network()
    start_port = int(input("Enter the start port (default 1): ") or 1)
    end_port = int(input("Enter the end port (default 1024): ") or 1024)

    result = network_scan(subnet, start_port, end_port)
    
    if result:
        print("\nOpen Ports Found:")
        for host, ports in result.items():
            print(f"{host}: {ports}")
    else:
        print("\nNo open ports found.")
