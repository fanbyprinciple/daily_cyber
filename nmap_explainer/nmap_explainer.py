import nmap
import google.generativeai as genai
import os

# 1. Setup your API Key
# Get a key from: https://aistudio.google.com/
API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def run_nmap_audit(target):
    nm = nmap.PortScanner()
    print(f"[*] Scanning {target}... this may take a minute.")
    # -sV for version detection
    nm.scan(target, arguments='-sV -T4')
    
    scan_summary = ""
    for host in nm.all_hosts():
        scan_summary += f"\nHost: {host} ({nm[host].state()})\n"
        for proto in nm[host].all_protocols():
            for port in sorted(nm[host][proto].keys()):
                s = nm[host][proto][port]
                scan_summary += f"Port: {port} | Service: {s['name']} | Product: {s.get('product','')} | Version: {s.get('version','')}\n"
    return scan_summary

def analyze_with_llm(scan_data):
    prompt = f"""
    You are a professional Cyber Security Auditor. 
    I have performed an Nmap scan on a test environment. 
    Please analyze the following scan results:
    
    {scan_data}
    
    Provide a report with:
    1. Criticality assessment (Low/Medium/High).
    2. Potential vulnerabilities associated with these specific service versions.
    3. Clear, step-by-step remediation advice for securing these services.
    4. Mention any ports that should absolutely not be exposed to the public internet.
    
    Be concise and professional.
    """
    
    print("[*] Sending data to LLM for analysis...")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # WARNING: Only scan targets you own (e.g., your local router or lab VM)
    target = "127.0.0.1" 
    
    raw_results = run_nmap_audit(target)
    
    if raw_results.strip():
        report = analyze_with_llm(raw_results)
        print("\n" + "="*50)
        print("AI SECURITY AUDIT REPORT")
        print("="*50)
        print(report)
    else:
        print("[!] No scan data found. Check if the target is up.")