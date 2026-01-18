import nmap

def run_nmap_audit(target):
    # Initialize the port scanner
    nm = nmap.PortScanner()
    
    print(f"--- Starting Security Audit for: {target} ---")
    
    # Run scan: -sV (Version detection), -T4 (Faster execution)
    # Note: Scanning targets you do not own is illegal.
    nm.scan(target, arguments='-sV -T4')

    report_data = []

    for host in nm.all_hosts():
        host_info = {
            "host": host,
            "status": nm[host].state(),
            "protocols": []
        }

        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                service = nm[host][proto][port]
                port_data = {
                    "port": port,
                    "state": service['state'],
                    "name": service['name'],
                    "product": service.get('product', 'Unknown'),
                    "version": service.get('version', 'Unknown'),
                    "extrainfo": service.get('extrainfo', '')
                }
                host_info["protocols"].append(port_data)
        
        report_data.append(host_info)

    return report_data

def print_summary(data):
    if not data:
        print("No data found or host is down.")
        return

    for entry in data:
        print(f"\n[HOST]: {entry['host']} ({entry['status'].upper()})")
        print("-" * 50)
        print(f"{'PORT':<8} {'STATE':<10} {'SERVICE':<15} {'VERSION'}")
        print("-" * 50)
        
        for p in entry['protocols']:
            version_str = f"{p['product']} {p['version']}"
            print(f"{p['port']:<8} {p['state']:<10} {p['name']:<15} {version_str}")

if __name__ == "__main__":
    # Replace with your local test IP or '127.0.0.1'
    target_ip = "127.0.0.1" 
    results = run_nmap_audit(target_ip)
    print_summary(results)