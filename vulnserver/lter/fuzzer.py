#!/usr/bin/python

from boofuzz import *
from sys import exit

host = '192.168.1.250'
port = 9999

def get_banner(target, my_logger, session, *args, **kwargs):
    banner_template = "Welcome to Vulnerable Server! Enter HELP for help."
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
	s_initialize("LTER")                             # This just gives the session the name, "TRUN"
	
	s_string("LTER", fuzzable = False)     # strings are fuzzable by default, so here I set it to 'false'
	s_delim(" ", fuzzable = False)             # dont want to fuzz the space between the 'TRUN' command and the buffer
	s_string("FUZZ")                                   # This is the parameter I want to fuzz
	s_static("\r\n")                                   # The final block hits enter for us.
	
	session.connect(s_get("LTER"), callback=get_banner)      # Connect to the server following the guidlines defined above. Set the callback function.
	session.fuzz()                                                                     # call the function to begin fuzzing
	
	
if __name__ == "__main__":
	main()