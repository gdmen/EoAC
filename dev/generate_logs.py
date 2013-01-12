"""
generate_logs.py
Saves AssaultCube client logs to file

Copyright 2012, gdm
"""
import threading
import time
import os
import urllib
import traceback
import Queue
import re
import sys
import subprocess
import signal

def main():
    """
    Script's entry point.
    
    """
    try:
        logfile = open('test'+str(time.time()), 'a')
        
        ac_client = subprocess.Popen('bin_win32/ac_client.exe',
                                     shell = False,
                                     stdin = subprocess.PIPE,
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.STDOUT)
        # Avoid having to re-interpret dot notation in the loop
        readline = ac_client.stdout.readline
        while True:
            next_line = readline()
            logfile.write(next_line + '\n')
            
    except KeyboardInterrupt:
        print 'Quitting . . .'
        ac_client.stdin.close()
        ac_client.stdout.close()
        ac_client.send_signal(signal.CTRL_C_EVENT)
        while not ac_client.poll() or not ac_client.poll() < 0:
            time.sleep(1)
            try:
                ac_client.terminate()
            except:
                logfile.write('UNEXPECTED (main): ac_server.terminate(): ' +
                      traceback.format_exc())
        ac_client.close()
        
if __name__ == '__main__':
    main()
