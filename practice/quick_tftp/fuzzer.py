#!/usr/bin/env python

from boofuzz import *
import time

def main():
        sesh = Session(
                sleep_time=1,
                target=Target(
                        connection=SocketConnection("192.168.1.29",69,proto='udp',bind=('0.0.0.0',17999))
                ),
        )

        s_initialize('get')
        s_binary('0002')
        s_string('file.txt')
        s_binary('00')
        s_string('netascii')
        s_binary('00')

        sesh.connect(s_get('get'))
        sesh.fuzz()

if __name__ == "__main__":
        main()