"""
jerboa.py
A convenience mod (wrapper) for the AssaultCube 1.1.0.4 client.
This wrapper reads the client's stdout and:
- Uploads screenshots to Imgur
- Updates the Jerboa database with screenshot data

Copyright 2013, gdm
"""
import j_config as c
from j_logger import *
from j_parser import *
from j_upload import *
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
        self.successful_post = False
        threading.Thread.__init__(self)
    
    def stop(self):
        self.successful_post = True

    def run(self):
        try:
            while not self.successful_post:
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
                    num_uploads = len(local_file_paths_json)
                    if num_uploads > 0:
                        prnt = 'Uploading ' + str(num_uploads) + ' prior screenshot'
                        if num_uploads != 1:
                            prnt += 's'
                        prnt += '. . .'
                        self.logger.debug(prnt, True)
                    for local_file_path in local_file_paths_json:
                        self.logger.debug('(' + self.log_identifier + '.run): ' +
                                          'FILE PATH: ' + local_file_path)
                        screenshot = BasicScreenshotData(
                                        local_file_path,
                                        self.config.user_id,
                                        self.config.upload_key)
                        self.imgur_queue.put(screenshot, True)
                    self.successful_post = True
                
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
        if len(post_response) > 0:
            self.logger.debug(self.log_identifier + ': POST RESPONSE ERROR')
            self.logger.debug(self.log_identifier + ': POST RESPONSE: ' +
                              str(post_response))
            return False
        else:
            self.out_queue.put(screenshot)
            self.logger.debug('Uploading ' +
                              str(os.path.basename(screenshot.local_file_path)), True)
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
        if len(post_response) > 0:
            self.logger.debug(self.log_identifier + ': POST RESPONSE ERROR')
            self.logger.debug(self.log_identifier + ': POST RESPONSE: ' +
                              str(post_response))
            return False
        else:
            self.logger.debug('Finished ' +
                              str(os.path.basename(screenshot.local_file_path)), True)
            return True



def main():
    """
    Script's entry point.
    """
    print c.APPLICATION_NAME + ' version ' + c.APPLICATION_VERSION

    is_debug = c.IS_DEBUG
    if len(sys.argv) > 4:
        print "That's too many command line args!"
        raw_input("Press Enter to Quit")
        return

    logfile_name = c.LOGFILE_PREFIX + str(time.time()) + c.LOGFILE_SUFFIX
    # Commandline debug flag
    if '-d' in sys.argv:
        is_debug = True
        print "Logging to file (" + logfile_name + ")."
    logger = Logger(c.LOG_DIR, logfile_name, is_debug)
    

    try:
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
        # If bash file was specified by user, use that instead
        # Might throw an IndexError
        if len(sys.argv) >= 3 and '-c' in sys.argv:
            client_bash = sys.argv[sys.argv.index('-c') + 1]
            print "Using specified bash file (" + client_bash + ")."
        if os.name == c.POSIX_OS_NAME:
            client_bash = './' + client_bash
        logger.debug('(main): client bash is ' + client_bash + '.')
    except IndexError:
        logger.debug('ERROR (main): ' + traceback.format_exc())
        print 'Most likely a command line parameter mistake: ',
        if is_debug:
            print 'see logfile (' + logfile_name + ').'
        else:
            print 're-run with logging enabled:'
            if os.name == c.POSIX_OS_NAME:
                print '> ./' + c.FILE_NAME_NIX +' -d'
                print '> ./' + c.FILE_NAME_NIX +' -d -c <custom config>'
            elif os.name == c.NT_OS_NAME:
                print '> ' + c.FILE_NAME_WIN +' -d'
                print '> ' + c.FILE_NAME_WIN +' -d -c <custom config>'
        logger.close()
        raw_input("Press Enter to Quit")
        return

    try:
        threads_initiated = False
        # Instantiate Parser
        parser = Parser(logger)
        # Read in configuration parameters
        parser.loadConfig(c.CONFIG_FILE)

        # Die if config parameters were not all there
        if not parser.config.complete():
            logger.debug('(main): ' + c.CONFIG_FILE + ' missing parameters.')
            print 'ERROR: missing configuration parameter in ' + c.CONFIG_FILE
            logger.close()
            raw_input("Press Enter to Quit")
            return

        # Only start up upload/dowload threads after getting config parameters
        # Instantiated in reverse order in order to link up input/output queues
        
        # ScreenshotUploadedThread (fourth stage)
        screenshot_uploaded_in_queue = Queue.Queue(maxsize=0)
        screenshot_uploaded_thread = ScreenshotUploadedThread(
                                        screenshot_uploaded_in_queue,
                                        parser.config,
                                        logger)
        screenshot_uploaded_thread.start();
        
        # ImmgurUploadThread (third stage)
        imgur_upload_in_queue = Queue.Queue(maxsize=0)
        imgur_upload_thread = ImgurUploadThread(imgur_upload_in_queue,
                                                screenshot_uploaded_in_queue,
                                                logger)
        imgur_upload_thread.start();
        
        # ScreenshotTakenThread (second stage)
        screenshot_taken_in_queue = Queue.Queue(maxsize=0)
        screenshot_taken_thread = ScreenshotTakenThread(
                                    screenshot_taken_in_queue,
                                    imgur_upload_in_queue,
                                    parser.config, logger)
        screenshot_taken_thread.start();
        
        # GetUnsentScreenshotsThread (first stage)
        get_unsent_screenshots_thread = GetUnsentScreenshotsThread(
                                            imgur_upload_in_queue,
                                            parser.config,
                                            logger)
        get_unsent_screenshots_thread.start();
        threads_initiated = True
    except IOError:
        logger.debug('ERROR (main): ' + traceback.format_exc())
        print 'Could not find required file: ',
        if is_debug:
            print 'see logfile (' + logfile_name + ').'
        else:
            print 're-run with logging enabled:'
            if os.name == c.POSIX_OS_NAME:
                print '> ./' + c.FILE_NAME_NIX +' -d'
                print '> ./' + c.FILE_NAME_NIX +' -d -c <custom config>'
            elif os.name == c.NT_OS_NAME:
                print '> ' + c.FILE_NAME_WIN +' -d'
                print '> ' + c.FILE_NAME_WIN +' -d -c <custom config>'
        print '. . .'
        if threads_initiated:
          get_unsent_screenshots_thread.stop()
          screenshot_taken_thread.stop()
          imgur_upload_thread.stop()
          screenshot_uploaded_thread.stop()
        logger.close()
        raw_input("Press Enter to Quit")
        return
       
    try:
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
        ac_client = subprocess.Popen(client_bash,
                                     shell = False,
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.STDOUT)
        # Avoid having to re-interpret dot notation in the loop
        ac_readline = ac_client.stdout.readline
        logger.debug('(main): Start parsing loop.')
        while True:
            line = ac_readline()
            if not line or ac_client.poll() != None:
                raise KeyboardInterrupt()
            parser.parseLine(line, screenshot_taken_in_queue)
            # Windows holds up the KeyboardInterrupt and this script never
            # receives it (without this sleep)
            # time.sleep(1)
            # BUT, with the sleep, the logs are parsed far too slowly >.>
            # Solution: No Ctrl-C for Windows.
    except OSError:
        logger.debug('ERROR (main): ' + traceback.format_exc())
        print 'Check your specified bash file: ',
        if is_debug:
            print 'see logfile (' + logfile_name + ').'
        else:
            print 're-run with logging enabled:'
            if os.name == c.POSIX_OS_NAME:
                print '> ./' + c.FILE_NAME_NIX +' -d'
                print '> ./' + c.FILE_NAME_NIX +' -d -c <custom config>'
            elif os.name == c.NT_OS_NAME:
                print '> ' + c.FILE_NAME_WIN +' -d'
                print '> ' + c.FILE_NAME_WIN +' -d -c <custom config>'
        print '. . .'
        get_unsent_screenshots_thread.stop()
        screenshot_taken_thread.stop()
        imgur_upload_thread.stop()
        screenshot_uploaded_thread.stop()
        logger.close()
        raw_input("Press Enter to Quit")
        return
    except KeyboardInterrupt:
        try:
          logger.debug('KeyboardInterrupt (main)')

          logger.debug('\nSaving screenshots, do not exit.', True)
          # Make sure we get any remaining output chilling in the subprocess's
          # output pipe
          while True:
              line = ac_readline()
              if not line:
                  break
              parser.parseLine(line, screenshot_taken_in_queue)

          remaining_uploads = screenshot_taken_in_queue.qsize() + imgur_upload_in_queue.qsize()
          prnt = str(remaining_uploads) + ' upload'
          if remaining_uploads != 1:
              prnt += 's'
          prnt += ' remaining, please wait . . .'
          logger.debug(prnt, True)

          # Close the log file when no longer running
          # Make sure all upload threads are done
          # (Don't want to interrupt an upload)
          # TODO: add a backoff here + a message ?
          while screenshot_taken_in_queue.qsize() > 0:
              time.sleep(0.01)
          screenshot_taken_thread.stop()
          while screenshot_taken_thread.isAlive():
              time.sleep(0.01)
          logger.debug('**All screenshots saved. It is now safe to exit**', True)
          # Finish all imgur uploads (could be time consuming!)
          while imgur_upload_in_queue.qsize() > 0:
              time.sleep(0.01)
          imgur_upload_thread.stop()
          while imgur_upload_thread.isAlive():
              time.sleep(0.01)

          # Finish all application website updates
          while screenshot_uploaded_in_queue.qsize() > 0:
              time.sleep(0.01)
          screenshot_uploaded_thread.stop()
          while screenshot_uploaded_thread.isAlive():
              time.sleep(0.01)
          
          while screenshot_taken_thread.isAlive() or imgur_upload_thread.isAlive() or screenshot_uploaded_thread.isAlive():
              time.sleep(0.01)
        except KeyboardInterrupt:
          get_unsent_screenshots_thread.stop()
          screenshot_taken_thread.stop()
          imgur_upload_thread.stop()
          screenshot_uploaded_thread.stop()
        finally:
            logger.close()

        
if __name__ == '__main__':
    main()
