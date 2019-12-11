#!/usr/bin/python

############################
## Vulnserver fuzzer!     ##
## Author: Robel Campbell ##
############################

import os
import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def usage():
	print '''

                   _        _        _______           _______  _______  _______  _______ 
|\     /||\     /|( \      ( (    /|(  ____ \|\     /|/ ___   )/ ___   )(  ____ \(  ____ )
| )   ( || )   ( || (      |  \  ( || (    \/| )   ( |\/   )  |\/   )  || (    \/| (    )|
| |   | || |   | || |      |   \ | || (__    | |   | |    /   )    /   )| (__    | (____)|
( (   ) )| |   | || |      | (\ \) ||  __)   | |   | |   /   /    /   / |  __)   |     __)
 \ \_/ / | |   | || |      | | \   || (      | |   | |  /   /    /   /  | (      | (\ (   
  \   /  | (___) || (____/\| )  \  || )      | (___) | /   (_/\ /   (_/\| (____/\| ) \ \__
   \_/   (_______)(_______/|/    )_)|/       (_______)(_______/(_______/(_______/|/   \__/
                                                                                          

A custom fuzzer for Vulnserver
By: Robel Campbell
'''
	print "Enter the IP, port and command you wish to fuzz.\n"
	print "Usage: python ", sys.argv[0], " <ip> <port> <command>\n"
	print "Example: python ", sys.argv[0], " 192.168.1.24 9999 HTER"

if (len(sys.argv) < 4 or len(sys.argv) > 4):
    usage()
    sys.exit()
else:
	while True:
		try:
			s.connect((str(sys.argv[1]), int(sys.argv[2])))
			print s.recv(1024)
			buff = 'A' * 50
			while True:
				try:
					print "Fuzzing with  " + str(len(buff)) + " bytes..."
					s.send(str(sys.argv[3]) + ' ' + buff +'\r\n')
					buff = buff + 'A' * 50
				except:
					print "[+] Crash occured with buffer length: " + str(len(buff)-50)
					sys.exit()
		except:
			print "Could not connect to the remote server!"
			sys.exit()
	

