#!/usr/bin/python

from boofuzz import *
from sys import exit

host = '192.168.1.36'
port = 21

# Checks if the connection is still open or if a banner is sent back. If not, the fuzzer quits. Good for stopping the script after crashing the program.
def get_banner(target, my_logger, session, *args, **kwargs):
    banner_template = "220 FTP Utility FTP server (Version 1.00) ready."
    try:
        banner = target.recv(10000)
    except:
        print "Unable to connect. Target is down. Exiting."
        exit(1)
 
    my_logger.log_check('Receiving banner..')
    if banner_template in banner:
        my_logger.log_pass('banner received')
    else:
        my_logger.log_fail('No banner received')
        print "No banner received, exiting.."
        exit(1)

def main():
	
	# Create the session and set the logging function
	session = Session(
		target=Target(
			connection = SocketConnection(host, port, proto='tcp'),
		)
	)
	
	# Define the parameters to fuzz.
	s_initialize("USER")	
	s_string("USER", fuzzable = False)     
	s_delim(" ", fuzzable = False)             
	s_string("anonymous", fuzzable = False)                                
	s_static("\r\n")                                
	
	s_initialize("PASS")	
	s_string("PASS", fuzzable = False)     
	s_delim(" ", fuzzable = False)             
	s_string("password", fuzzable = False)                                
	s_static("\r\n")
	
	s_initialize("CWD")	
	s_string("CWD", fuzzable = False)     
	s_delim(" ", fuzzable = False)             
	s_string("FUZZ")                                
	s_static("\r\n")
	
	session.connect(s_get("USER"), callback=get_banner)
	session.connect(s_get("USER"), s_get("PASS"))
	session.connect(s_get("PASS"), s_get("CWD"))
	session.fuzz()                                                                     # call the function to begin fuzzing
	
	
if __name__ == "__main__":
	main()