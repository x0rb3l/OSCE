#!/usr/bin/python

from boofuzz import *
from sys import exit

host = '192.168.1.29'
port = 21

# Checks if the connection is still open or if a banner is sent back. If not, the fuzzer quits. Good for stopping the script after crashing the program.
def get_banner(target, my_logger, session, *args, **kwargs):
    banner_template = "220 Hello, I'm freeFTPd 1.0"
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
		),
		
	)
	
	
	s_initialize("user")
	s_string("USER", fuzzable=False)
	s_delim(" ", fuzzable=False)
	s_string("user", fuzzable=False)
	s_static("\r\n")

	s_initialize("pass")
	s_string("PASS", fuzzable=False)
	s_delim(" ", fuzzable=False)
	s_string(",FUZZ")
	s_static("\r\n")

	session.connect(s_get("user"), callback=get_banner)
	session.connect(s_get("user"), s_get("pass"))
	
	session.fuzz()                                                               # call the function to begin fuzzing
	
	
if __name__ == "__main__":
	main()