getting rsa.pub from smbclient

smb pentesting

SMV,
FTP
TELNET
NFS
SMPTP
MYSQL

tryhackme labs
network services

Enumeration

domain
users
groups

how are they interconnected

ldapsearch

# using evil-winrm to connect

inside the ad, the user can be enumerated by enum4linux and ldapsearch

using bloodhoudn with evilwinrm

bloodhougn downloads

download Sharphound.exe

sharphound -c all


get the zip and upload it into bloodhound

web exploitation

Task of the day:

    https://tryhackme.com/r/room/networkservices
    https://tryhackme.com/r/room/networkservices2
    Optional: https://tryhackme.com/r/room/easyctf
    AD Basics https://tryhackme.com/r/room/winadbasics
    BloodHound using https://github.com/SpecterOps/BloodHound/wiki/Example-Data


sudo responder -i eth0


llmnr query
\\hackme - this weill 

https://tcm-sec.com/llmnr-poisoning-and-how-to-prevent-it/

ldapdomain dump

all the systems would have sid amdid 
sid will be common for all the users

ldapsearch -x -b "dc=devconnected,dc=com" -H ldap://192.168.178.29

bloodhound-python -u administrator -p Password@123 -ns 192.1681.195 -d iglite.local All

crackmapexec smb 192.168.1.0/24 -u administrator -d iglite.local -p Password@123

impacket


pwnd using crackmapexec
the user was pwnd now we will dump all the data

# researching on AD

![](pentest_ad_dark_2023_02.svg)

https://github.com/senderend/hackbook


https://github.com/Tib3rius/AutoRecon

