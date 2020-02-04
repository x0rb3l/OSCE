#!/usr/bin/python

from boofuzz import *
from sys import exit

host = '192.168.1.250'
port = 80

# Checks if the connection is still open or if a banner is sent back. If not, the fuzzer quits. Good for stopping the script after crashing the program.
def get_banner(target, my_logger, session, *args, **kwargs):
    banner_template = "Please enter your username and password to login"
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
	
	# Create logging function. Outputs to a .csv file
	csv_log = open('fuzz_results.csv', 'wb') ## create a csv file
	my_logger = [FuzzLoggerCsv(file_handle=csv_log)] ### create a FuzzLoggerCSV object with the file handle of our csv file
	
	# Create the session and set the logging function
	session = Session(
		target=Target(
			connection = SocketConnection(host, port, proto='tcp'),
		),
		fuzz_loggers=my_logger, ## set my_logger (csv) as the logger for the session
	)
	
	# Define the parameters to fuzz.
	s_initialize(name="Request")
	with s_block("Request-Line"):
		s_group("Method", ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
		s_delim(" ", name='space-1', fuzzable = False)
		s_string("/login.htm", name='Request-URI')
		s_delim(" ", name='space-2', fuzzable = False)
		s_string('HTTP/1.1', name='HTTP-Version', fuzzable = False)
		s_static("\r\n", name="Request-Line-CRLF")
	s_static("\r\n", "Request-CRLF")

	session.connect(s_get("Request"))

	session.fuzz()                                                 # call the function to begin fuzzing

if __name__ == "__main__":
	main()