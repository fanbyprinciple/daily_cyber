import nmap
import google.generativeai as genai
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURATION ---
# Get a key from: https://aistudio.google.com/
API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class SecurityReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "AI-Generated Security Audit Report", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def run_nmap_audit(target):
    nm = nmap.PortScanner()
    print(f"[*] Scanning {target}...")
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
    Act as a Senior Cybersecurity Consultant. Analyze these Nmap results:
    {scan_data}
    
    Format the report with these exact headings:
    1. EXECUTIVE SUMMARY
    2. KEY VULNERABILITIES
    3. REMEDIATION PLAN
    4. CRITICALITY SCORE (1-10)
    
    Be specific about version-related CVEs. Keep it professional.
    """
    print("[*] Analyzing with AI...")
    response = model.generate_content(prompt)
    return response.text

def create_pdf(report_text, filename="Security_Audit.pdf"):
    pdf = SecurityReport()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Cleaning text for PDF (removing common illegal characters)
    clean_text = report_text.encode('latin-1', 'replace').decode('latin-1')
    
    # Multi-cell handles text wrapping automatically
    pdf.multi_cell(0, 10, clean_text)
    
    pdf.output(filename)
    print(f"[+] Report saved as: {filename}")

if __name__ == "__main__":
    target_ip = "127.0.0.1" # Change to your target
    
    raw_data = run_nmap_audit(target_ip)
    
    if raw_data.strip():
        ai_report = analyze_with_llm(raw_data)
        create_pdf(ai_report)
    else:
        print("[!] No results. Host might be down.")