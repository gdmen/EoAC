"""
jerboa.py
A convenience mod (wrapper) for the AssaultCube 1.1.0.4 client.
This wrapper reads the client's stdout and:
- Uploads screenshots to Imgur
- Updates the Jerboa database with screenshot data

Copyright 2013, gdm
"""

import config as c
from logger import Logger
from parser import *
from upload import *
import threading
import time
import os
import traceback
import Queue
import sys
import subprocess
import signal
import base64
import json


class GetUnsentScreenshotsThread(threading.Thread):
    """
    GetUnsentScreenshotsThread gets a list of local_file_paths corresponding
    to screenshots that still need to be uploaded to Imgur & Jerboa

    GetUnsentScreenshotsThread then instantiates ScreenshotData elements and
    pushes them into the normal queue process for uploads (skipping the normal
    first step of parsing AC client logs)
    """
    def __init__(self, imgur_queue, config, logger):
        self.imgur_queue = imgur_queue
        self.config = config
        self.upload_url = c.GET_UNSENT_SCREENSHOTS_URL
        self.log_identifier = 'GetUnsentScreenshotsThread'
        self.logger = logger
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            successful_post = False
            while not successful_post:
                post_response = post(self.upload_url,
                                     {'user_id' : self.config.user_id,
                                      'upload_key' : self.config.upload_key},
                                     self.logger)
                if post_response == False:
                    continue

                post_response = post_response.read()
                self.logger.debug('POST RESPONSE: ' + str(post_response))
                local_file_paths_json = json.loads(post_response)
                self.logger.debug('JSON RESPONSE: ' +
                                  str(local_file_paths_json))

                if not local_file_paths_json == None:
                    for local_file_path in local_file_paths_json:
                        self.logger.debug('(' + self.log_identifier + '.run): ' +
                                          'FILE PATH: ' + local_file_path)
                        screenshot = BasicScreenshotData(
                                        local_file_path,
                                        self.config.user_id,
                                        self.config.upload_key)
                        self.imgur_queue.put(screenshot, True)
                    successful_post = True
                
        except ValueError:
            self.logger.debug('UNEXPECTED NON-JSON RESPONSE.')
            return False
        except:
            self.logger.debug(self.log_identifier + 'ERROR unexpected: ' +
                              traceback.format_exc())
            raise


class ScreenshotTakenThread(AbstractUploadThread):
    def __init__(self, in_queue, out_queue, config, logger):
        super(ScreenshotTakenThread, self).__init__(in_queue,
                                                    c.TAKEN_SCREENSHOT_URL,
                                                    'ScreenshotTakenThread',
                                                    logger)
        self.out_queue = out_queue
        self.config = config
        
    def posterize(self, screenshot):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        post_array = {'upload_key' : self.config.upload_key,
                      'user_id' : self.config.user_id,
                      'local_file_path' : screenshot.local_file_path,
                      'ac_map' : screenshot.ac_map,
                      'ac_mode' : screenshot.ac_mode,
                      'ac_mastermode' : screenshot.ac_mastermode,
                      'ac_ip' : screenshot.ac_ip,
                      'ac_port' : screenshot.ac_port,
                      'ac_minutes_remaining' : screenshot.ac_minutes_remaining,
                      'ac_players' : screenshot.ac_players,
                      'title' : screenshot.title,
                      'caption' : screenshot.caption,
                      'tags' : screenshot.tags}

        # TODO: Perhaps find a more extensible way of handling this
        if isinstance(screenshot, BlacklistScreenshotData):
            post_array['blacklist_name'] = screenshot.name
            post_array['blacklist_ip'] = screenshot.ip
            post_array['blacklist_reason'] = screenshot.reason

        return post_array
        
    def handle_response(self, screenshot, post_response):
        """
        Handles the response from POST.
        Returns TRUE on expected response, FALSE for a retry
        """
        self.out_queue.put(screenshot)
        return True


class ImgurUploadThread(AbstractUploadThread):
    def __init__(self, in_queue, out_queue, logger):
        super(ImgurUploadThread, self).__init__(in_queue,
                                                c.IMGUR_UPLOAD_URL,
                                                'ImgurUploadThread', logger)
        self.out_queue = out_queue
        
    def posterize(self, screenshot):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        # Convert image to base64
        source = open(screenshot.local_file_path, 'rb')
        self.logger.debug('ss_data.local_file_path: ' +
                          screenshot.local_file_path)
        screenshot_base64 = base64.b64encode(source.read())
        return {'key' : c.IMGUR_API_KEY,
                'image' : screenshot_base64}  
        
    def handle_response(self, screenshot, post_response):
        """
        Handles the response from POST.
        Returns TRUE on expected response, FALSE for a retry
        """
        try:
            imgur_json = json.loads(post_response)
            self.logger.debug('JSON RESPONSE: ' + str(imgur_json))

            if imgur_json == None or 'error' in imgur_json:
                self.logger.debug('JSON RESPONSE ERROR.')
                return False
            elif 'upload' in imgur_json:
                self.logger.debug('JSON RESPONSE SUCCESS.')
                self.logger.debug('(' + self.log_identifier + '.run): ' +
                                  screenshot.local_file_path + ' to imgur: ' +
                                  str(time.time()))
                screenshot.imgur_hash = imgur_json['upload']['image']['hash']
                screenshot.imgur_delete_hash = imgur_json['upload']['image']['deletehash']
                # Push to queue that updates Jerboa with imgur hashes
                self.out_queue.put(screenshot)
                return True
            else:
                self.logger.debug('UNEXPECTED JSON RESPONSE.')
                return False
        except ValueError:
            self.logger.debug('UNEXPECTED NON-JSON RESPONSE.')
            return False


class ScreenshotUploadedThread(AbstractUploadThread):
    def __init__(self, in_queue, config, logger):
        super(ScreenshotUploadedThread, self).__init__(
            in_queue, c.UPLOADED_SCREENSHOT_URL,
            'ScreenshotUploadThread', logger)
        self.config = config
        
    def posterize(self, screenshot):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        self.logger.debug('LOCAL FILE PATH, UPLOADED THREAD: ' +
                          screenshot.local_file_path)
        return {'upload_key' : self.config.upload_key,
                'user_id' : self.config.user_id,
                'local_file_path' : screenshot.local_file_path,
                'imgur_hash' : screenshot.imgur_hash,
                'imgur_delete_hash' : screenshot.imgur_delete_hash}
        
    def handle_response(self, screenshot, post_response):
        """
        Handles the response from POST.
        Returns TRUE on expected response, FALSE for a retry
        """
        return True


def main():
    """
    Script's entry point.
    """
    logfile_name = c.LOGFILE_PREFIX + str(time.time()) + c.LOGFILE_SUFFIX
    logger = Logger(c.LOG_DIR, logfile_name, c.IS_DEBUG)

    if len(sys.argv) > 2:
        logger.debug('ERROR (main): more than one command line parameter.')
        sys.exit(2)

    # Only attempt to close the client if the client has been started
    ac_client_started = False
    try:
        # Instantiate Parser
        parser = Parser(logger)
        # Read in configuration parameters
        parser.loadConfig(c.CONFIG_FILE)

        # Die if config parameters were not all there
        if not parser.config.complete():
            logger.debug('(main): ' + c.CONFIG_FILE + ' missing parameters.')
            print 'ERROR: missing configuration parameter in ' + c.CONFIG_FILE
            logger.close()
            return

        # Only start up upload/dowload threads after getting config parameters
        # Instantiated in reverse order in order to link up input/output queues
        
        # ScreenshotUploadedThread (fourth stage)
        screenshot_uploaded_in_queue = Queue.Queue(maxsize=0)
        screenshot_uploaded_thread = ScreenshotUploadedThread(
                                        screenshot_uploaded_in_queue,
                                        parser.config,
                                        logger)
        
        # ImmgurUploadThread (third stage)
        imgur_upload_in_queue = Queue.Queue(maxsize=0)
        imgur_upload_thread = ImgurUploadThread(imgur_upload_in_queue,
                                                screenshot_uploaded_in_queue,
                                                logger)
        
        # ScreenshotTakenThread (second stage)
        screenshot_taken_in_queue = Queue.Queue(maxsize=0)
        screenshot_taken_thread = ScreenshotTakenThread(
                                    screenshot_taken_in_queue,
                                    imgur_upload_in_queue,
                                    parser.config, logger)
        
        # GetUnsentScreenshotsThread (first stage)
        get_unsent_screenshots_thread = GetUnsentScreenshotsThread(
                                            imgur_upload_in_queue,
                                            parser.config,
                                            logger)
        # Find and load bash file
        logger.debug('(main): NT bash: ' + c.NT_DEFAULT_BASH_FILE)
        logger.debug('(main): POSIX bash: ' + c.POSIX_DEFAULT_BASH_FILE)
        # Set the default bash file based on OS
        client_bash = c.POSIX_DEFAULT_BASH_FILE
        if os.name == c.POSIX_OS_NAME:
            logger.debug('(main): OS is POSIX.')
        elif os.name == c.NT_OS_NAME:
            client_bash = c.NT_DEFAULT_BASH_FILE
            logger.debug('(main): OS is NT.')
        else:
            logger.debug('UNEXPECTED (main): OS is ' + os.name + '.')
        # If bash file was input, use that instead
        if len(sys.argv) == 2:
            client_bash = sys.argv[1]
        logger.debug('(main): client bash is ' + client_bash + '.')
        
        """
        bash = open(client_bash)
        ac_client = None
        for cmd in bash:
            cmd = cmd.strip()
            logger.debug('(main): cmd: ' + cmd)
            if not cmd == "pause" and not cmd.startswith("#"):
                if ".exe" in cmd:
                    #cmd = '"' + os.getcwd() + '\\' + cmd[:cmd.find('.exe')+4] + '"' + cmd[cmd.find('.exe')+4:]
                    ac_client = subprocess.Popen(cmd,
                                                 shell = False,
                                                 stdin = subprocess.PIPE,
                                                 stdout = subprocess.PIPE,
                                                 stderr = subprocess.STDOUT)
                    ac_client_started = True
                # Funny story - this condition is here to prevent
                # unintentional forkbombs =/
                elif not 'jerboa.py' in cmd:
                    os.popen(cmd)
        """
        ac_client = subprocess.Popen('./' + client_bash,
                                     shell = False,
                                     stdin = subprocess.PIPE,
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.STDOUT)
        print c.APPLICATION_NAME
        print "Ctrl-C to exit"
        # Avoid having to re-interpret dot notation in the loop
        ac_readline = ac_client.stdout.readline
        logger.debug('(main): Start parsing loop.')

        while True:
            parser.parseLine(ac_readline(), screenshot_taken_in_queue)
            
    except IOError:
        logger.debug('ERROR (main): ' + traceback.format_exc())
        print 'Could not find required file: ',
        if c.IS_DEBUG:
            print 'see logfile (' + logfile_name + ').'
        else:
            print 're-run with logging enabled:'
            print '> python jerboa.py 1'
    except KeyboardInterrupt:
        print '\nFinishing uploads, please wait . . .'
        if ac_client_started:
            ac_client.stdin.close()
            ac_client.stdout.close()
            ac_client.send_signal(signal.CTRL_C_EVENT)
            while not ac_client.returncode:
                try:
                    ac_client.kill()
                    time.sleep(c.EXIT_RETRY_INTERVAL)
                except:
                    logger.debug('UNEXPECTED (main): ac_client.kill(): ' +
                          traceback.format_exc())
                    logger.debug('UNEXPECTED (main): ac_client.returncode: ' +
                          str(ac_client.returncode))
                    break
        
        # Close the log file when no longer running
        # Make sure all upload threads are done
        # (Don't want to interrupt an upload)
        # TODO: add a backoff here + a message
        while screenshot_taken_in_queue.qsize() > 0:
            time.sleep(1)
        screenshot_taken_thread.stop()

        # imgur uploads are time consuming, so finish the current upload
        # and leave the rest for the next time jerboa is run
        imgur_upload_thread.stop()
        # Stay here until the screenshot_upload_in_queue has been updated
        while imgur_upload_thread.isAlive():
            time.sleep(1)

        while screenshot_uploaded_in_queue.qsize() > 0:
            time.sleep(1)
        screenshot_uploaded_thread.stop()
        
        while screenshot_taken_thread.isAlive() or screenshot_uploaded_thread.isAlive():
            time.sleep(1)
        
        logger.close()

        
if __name__ == '__main__':
    main()
