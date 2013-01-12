"""
logger.py
This file contains classes and methods used by jerboa.py
- Logger

Copyright 2013, gdm
"""

import os

class Logger():
    """
    Logger is synchronous since it is important to have the most recent
    messages printed in the event of a crash.
    Currently, Logger only creates files and logs if 'is_debug'.
    """

    def __init__(self, logdir_name, logfile_name, is_debug):
        """
        Parameters:
            logdir_name = <string> child dir of pwd
            logfile_name = <string> name of logfile
        """
        self.is_debug = is_debug
        self.logfile = self.createLogFile(logdir_name, logfile_name)
        self.msg_length = 256

    def close(self):
        if self.is_debug:
            self.logfile.close()

    def createLogFile(self, logdir_name, logfile_name):
        """
        Creates 'logdir_name' and saves 'logfile_name' there if 'self.is_debug'
        Returns:
            File handle on successs
            False on failure
        """
        if self.is_debug:
            filehandle = None
            try:
                if not logdir_name in os.listdir('.'):
                    os.mkdir(logdir_name)
                filehandle = open(logdir_name + '/' + logfile_name, 'a')
            except:
                raise
            else:
                return filehandle
        return False

    def debug(self, msg):
        """
        Parameters:
            msg = <string> message to print
        """
        if self.is_debug:
            self.write(msg)

    def write(self, msg):
        """
        Only writes the first 'self.msg_length' characters of each 'msg' into
        'self.logfile' in order to avoid unreadable logs.
        """
        try:
            if not self.logfile.closed:
                self.logfile.write(msg[:self.msg_length] + '\n')
            else:
                print ('ERROR (Logger.write):' +
                      ' logfile = ' + self.logfile.name +
                      ' msg = ' + msg +
                      ' file was probably closed!')
        except:
            print ('ERROR UNEXPECTED (Logger.write):')
            raise
