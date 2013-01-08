"""
jerboa.py
A convenience mod (wrapper) for the AssaultCube 1.1.0.4 client.
This wrapper reads the client's stdout and:
- Uploads screenshots to Imgur
- Updates the Jerboa database with screenshot data

Copyright 2013, gdm
"""

import constants as c
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
import base64
import json

# Needed to maintain parsing state.
ss_in_progress = False
ac_map = 'unknown'
ac_mode = '0'
ac_mastermode = '0'
ac_ip = ''
ac_port = ''
ac_minutes_remaining = 0
ac_players = []

blacklist = False
blacklist_reason = 'reason'
blacklist_name = 'name'
blacklist_ip = '127.0.0.1'

most_recent_ss_name = ''

user_id = None
upload_key = None

def createLogFile(filename):
    """
    Creates <c.LOG_DIR> and saves log file there if c.IS_DEBUG
    Returns:
        File handle on success
        False on failure
    """
    if c.IS_DEBUG:
        filehandle = None
        try:
            if not c.LOG_DIR in os.listdir('.'):
                os.mkdir(c.LOG_DIR)
            filehandle = open(c.LOG_DIR + '/' + filename, 'a')
        except:
            raise
        else:
            return filehandle
    return False


def debug(logfile, string):
    """
    Logs 'string' to 'logfile' if <c.IS_DEBUG>
    """
    if c.IS_DEBUG:
        try:
            if not logfile.closed:
                logfile.write(string[:256] + '\n')
        except:
            print ('ERROR UNEXPECTED (debug):' +
                  ' logfile = ' + logfile.name +
                  ' string = ' + string +
                  ' file was probably closed!')
            raise


def post(url, params, logfile):
    """
    Http POSTs 'params' to 'url'
    Expects 'params' in a map formatted like:
        {name(string):value(string)}
    Returns:
        Result on success
        False on failure
    """
    debug(logfile, '(post): url = ' + url)
    try:
        for key, value in params.items():
            params[key] = str(value)
            debug(logfile, '(post): ' + key + ' = ' + params[key][:32])
        debug(logfile, '(post): ' + urllib.urlencode(params))
        return urllib.urlopen(url, urllib.urlencode(params))
    except IOError, e:
        debug(logfile, 'ERROR (post): ' + traceback.format_exc())
        print 'Failure to connect to a ' + c.APPLICATION_NAME + ' server . . .'
        return False
    except:
        debug(logfile, 'ERROR UNEXPECTED (post): ' + traceback.format_exc())
        #raise

        
class BasicScreenshotData(object):
    def __init__(self, local_file_path, user_id, key):
        self.local_file_path = local_file_path
        self.user_id = user_id
        self.key = key
        self.imgur_hash = ''
        self.imgur_delete_hash = ''
        # Some metrics to report to Jerboa
        # self.imgur_attempt_count = 0

class ScreenshotData(BasicScreenshotData):
    def __init__(self, local_file_path, user_id, key, ac_map, ac_mode,
                 ac_mastermode, ac_ip, ac_port, ac_minutes_remaining,
                 ac_players, title = 'title', caption = 'caption', tags = ''):
        super(ScreenshotData, self).__init__(local_file_path, user_id, key)
        self.ac_map = ac_map
        self.ac_mode = ac_mode
        self.ac_mastermode = ac_mastermode
        self.ac_ip = ac_ip
        self.ac_port = ac_port
        self.ac_minutes_remaining = ac_minutes_remaining
        self.ac_players = ac_players
        self.title = title
        self.caption = caption
        # csv string of tags
        self.tags = tags
        self.imgur_hash = ''
        self.imgur_delete_hash = ''


class BlacklistScreenshotData(ScreenshotData):
    def __init__(self, local_file_path, user_id, key, ac_map, ac_mode,
                 ac_mastermode, ac_ip, ac_port, ac_minutes_remaining,
                 ac_players, name, ip, reason,
                 title = 'title', caption = 'caption', tags = ''):
        super(BlacklistScreenshotData, self).__init__(local_file_path, user_id, key,
                                                      ac_map, ac_mode, ac_mastermode,
                                                      ac_ip, ac_port,
                                                      ac_minutes_remaining,
                                                      ac_players,
                                                      title, caption, tags)
        self.name = name
        self.ip = ip
        self.reason = reason


class AbstractUploadThread(threading.Thread):
    """
    AbstractUploadThread is not meant to be instantiated.
    AbstractUploadThread POSTs messages from a given queue to a given url.
    On succesive <c.STATS_UPDATE_INTERVAL> intervals:
        Pulls a new element from the in_queue and POSTs the parameters to
        the upload_url.
        If POST fails, pushes element back on top of the queue.
        Backs off on successive failures.
    """
    def __init__(self, in_queue, upload_url, log_name, logfile):
        self.in_queue = in_queue
        self.upload_url = upload_url
        self.log_name = log_name
        self.running = True
        # b_ are backoff variables
        # The run method's loop always sleeps for c.UPDATE_INTERVAL, but the
        # backoff procedure alters the number of loops made before action.
        # e.g. if b_post_freq is 20, the run loop will loops 20 times with no
        # action other than sleeping for c.UPDATE_INTERVAL
        # This is a bit cleaner than saving and comparing times between posts
        self.b_counter = 0
        self.b_last_post = 0
        self.b_post_freq = 1
        self.logfile = logfile
        threading.Thread.__init__(self)
        # self-starting thread
        self.start()
    
    def backoff(self):
        if self.b_post_freq <= (c.MAX_UPDATE_BACKOFF - c.UPDATE_BACKOFF_INCREMENT):
            self.b_post_freq += c.UPDATE_BACKOFF_INCREMENT
        debug(self.logfile, '(' + self.log_name +
              '.backoff): new interval = '
              + str(self.b_post_freq) + ' seconds')
        
    def posterize(self, element):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        raise NotImplementedError("Should have implemented this")
        
    def handle_response(self, element, post_response):
        """
        Handles the response from POST.
        Returns TRUE on expected response, FALSE for a retry
        """
        raise NotImplementedError("Should have implemented this")
    
    def run(self):
        while self.running:
            time.sleep(c.UPDATE_INTERVAL)
            try:
                self.b_counter += 1
                if self.b_counter - self.b_last_post >= self.b_post_freq:
                    # Get the next element to POST
                    # get_nowait() throws an empty queue exception - this is
                    # caught and ignored (if it blocks here, we may not be able to
                    # end this thread gracefully)
                    element = self.in_queue.get_nowait()

                    # Flag to know if upload was successful
                    # i.e. if element should be put back in queue
                    successful_post = True

                    post_response = post(self.upload_url,
                                         self.posterize(element),
                                         self.logfile)
                    # If POST failed to connect to server
                    if post_response == False:
                        successful_post = False
                        debug(self.logfile, self.log_name + ': POST FALSE')
                    else:
                        post_response = post_response.read()
                        debug(self.logfile, self.log_name + ': POST TRUE')
                        debug(self.logfile, self.log_name + ': POST RESPONSE: ' + str(post_response))
                        successful_post = self.handle_response(element, post_response)
                                                
                    debug(self.logfile, self.log_name + ': queue size: ' +
                          str(self.in_queue.qsize()))

                    if not successful_post:
                        # If POST failed for any reason, put element back into
                        # queue and increase the backoff time
                        self.in_queue.put(element, True)
                        self.backoff()
                        debug(self.logfile, '(' + self.log_name +
                              '.run) backing off.')
            except Queue.Empty:
                # Want to loop rather than blocking for the queue, so ignore
                # this
                continue
            except:
                debug(self.logfile, self.log_name + 'ERROR unexpected: ' +
                      traceback.format_exc())
                raise
        
    def stop(self):
        self.running = False


class ScreenshotTakenThread(AbstractUploadThread):
    def __init__(self, in_queue, out_queue, logfile):
        super(ScreenshotTakenThread, self).__init__(in_queue,
                                                c.TAKEN_SCREENSHOT_URL,
                                                'ScreenshotTakenThread', logfile)
        self.out_queue = out_queue
        
    def posterize(self, screenshot):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        post_array = {'key' : screenshot.key,
                      'id' : screenshot.user_id,
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
    def __init__(self, in_queue, out_queue, logfile):
        super(ImgurUploadThread, self).__init__(in_queue,
                                                c.IMGUR_UPLOAD_URL,
                                                'ImgurUploadThread', logfile)
        self.out_queue = out_queue
        
    def posterize(self, screenshot):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        # Convert image to base64
        source = open(screenshot.local_file_path, 'rb')
        debug(self.logfile, 'ss_data.local_file_path: ' + screenshot.local_file_path)
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
            debug(self.logfile, 'JSON RESPONSE: ' + str(imgur_json))

            if imgur_json == None or 'error' in imgur_json:
                debug(self.logfile, 'JSON RESPONSE ERROR.')
                return False
            elif 'upload' in imgur_json:
                debug(self.logfile, 'JSON RESPONSE SUCCESS.')
                debug(self.logfile, '(' + self.log_name + '.run): ' +
                      screenshot.local_file_path + ' to imgur: ' + str(time.time()))
                screenshot.imgur_hash = imgur_json['upload']['image']['hash']
                screenshot.imgur_delete_hash = imgur_json['upload']['image']['deletehash']
                # Push to queue for updating Jerboa with imgur hashes
                self.out_queue.put(screenshot)
                return True
            else:
                debug(self.logfile, 'UNEXPECTED JSON RESPONSE.')
                return False
        except ValueError:
            debug(self.logfile, 'UNEXPECTED NON-JSON RESPONSE.')
            return False


class ScreenshotUploadedThread(AbstractUploadThread):
    def __init__(self, in_queue, logfile):
        super(ScreenshotUploadedThread, self).__init__(in_queue,
                                                c.UPLOADED_SCREENSHOT_URL,
                                                'ScreenshotUploadThread', logfile)
        
    def posterize(self, screenshot):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        debug(self.logfile, 'LOCAL FILE PATH, UPLOADED THREAD: ' + screenshot.local_file_path)
        return {'key' : screenshot.key,
                'id' : screenshot.user_id,
                'local_file_path' : screenshot.local_file_path,
                'imgur_hash' : screenshot.imgur_hash,
                'imgur_delete_hash' : screenshot.imgur_delete_hash}
        
    def handle_response(self, screenshot, post_response):
        """
        Handles the response from POST.
        Returns TRUE on expected response, FALSE for a retry
        """
        return True


class GetUnsentScreenshotsThread(threading.Thread):
    """
    GetUnsentScreenshotsThread gets a list of local_file_paths corresponding
    to screenshots that still need to be uploaded to Imgur & Jerboa

    GetUnsentScreenshotsThread then instantiates ScreenshotData elements and
    pushes them into the normal queue process for uploads (skipping the first step)
    """
    def __init__(self, imgur_queue, logfile):
        self.imgur_queue = imgur_queue
        self.upload_url = c.GET_UNSENT_SCREENSHOTS_URL
        self.log_name = 'GetUnsentScreenshotsThread'
        self.logfile = logfile
        threading.Thread.__init__(self)
    
    def run(self):
        global user_id, upload_key
        try:
            successful_post = False
            while not successful_post:
                post_response = post(self.upload_url,
                                     {'id' : user_id,
                                      'key' : upload_key},
                                     self.logfile)
                if post_response == False:
                    continue

                post_response = post_response.read()
                debug(self.logfile, 'POST RESPONSE: ' + str(post_response))
                local_file_paths_json = json.loads(post_response)
                debug(self.logfile, 'JSON RESPONSE: ' + str(local_file_paths_json))

                if not local_file_paths_json == None:
                    for local_file_path in local_file_paths_json:
                        debug(self.logfile, '(' + self.log_name + '.run): ' +'FILE PATH: ' + local_file_path)
                        screenshot = BasicScreenshotData(local_file_path, user_id, upload_key)
                        self.imgur_queue.put(screenshot, True)
                
                successful_post = True
                
        except ValueError:
            debug(self.logfile, 'UNEXPECTED NON-JSON RESPONSE.')
            return False
        except:
            debug(self.logfile, self.log_name + 'ERROR unexpected: ' +
                  traceback.format_exc())
            raise


def main():
    """
    Script's entry point.
    
    """
    main_logfile = createLogFile(c.LOGFILE_PREFIX +
                                 str(time.time()) +
                                 c.LOGFILE_SUFFIX)
    debug(main_logfile, '(main): test write.')

    if len(sys.argv) > 2:
        debug(main_logfile, 'ERROR (main): more than one command line parameter.')
        sys.exit(2)

    # To avoid trying to close the client if jerboa exits before starting client
    ac_client_started = False
    try:
        # Read in configuration parameters
        debug(main_logfile, '(main): autoexec config: ' + c.CONFIG_FILE)
        config = open(c.CONFIG_FILE, 'r')
        for line in config:
            debug(main_logfile, '(main): autoexec config line: ' + line)
            if parseConfigLine(line, main_logfile):
                break
            
        # Die if config parameters were not all there
        if user_id == None or upload_key == None:
            debug(main_logfile, '(main): Jerboa config missing parameter.')
            print 'ERROR: missing configuration parameter in ' + c.CONFIG_FILE
            main_logfile.close()
            return
        
        # Only start up upload/dowload threads after getting config parameters
        # Instantiated in reverse order in order to link up input/output queues
        
        # ScreenshotUploadThread (fourth stage)
        screenshot_uploaded_queue = Queue.Queue(maxsize=0)
        screenshot_uploaded_thread = ScreenshotUploadedThread(screenshot_uploaded_queue, main_logfile)
        
        # ImmgurUploadThread (third stage)
        imgur_upload_queue = Queue.Queue(maxsize=0)
        imgur_upload_thread = ImgurUploadThread(imgur_upload_queue, screenshot_uploaded_queue, main_logfile)
        
        # ScreenshotTakenThread (second stage)
        screenshot_taken_queue = Queue.Queue(maxsize=0)
        screenshot_taken_thread = ScreenshotTakenThread(screenshot_taken_queue, imgur_upload_queue, main_logfile)
        
        # GetUnsentScreenshotsThread (first stage)
        get_unsent_screenshots_thread = GetUnsentScreenshotsThread(imgur_upload_queue, main_logfile)

    
        debug(main_logfile, '(main): NT bash: ' + c.NT_DEFAULT_BASH_FILE)
        debug(main_logfile, '(main): POSIX bash: ' + c.POSIX_DEFAULT_BASH_FILE)
        # Set the default bash file based on OS
        client_bash = c.POSIX_DEFAULT_BASH_FILE
        if os.name == c.POSIX_OS_NAME:
            debug(main_logfile, '(main): OS is POSIX.')
        elif os.name == c.NT_OS_NAME:
            client_bash = c.NT_DEFAULT_BASH_FILE
            debug(main_logfile, '(main): OS is NT.')
        else:
            debug(main_logfile, 'UNEXPECTED (main): OS is ' + os.name + '.')
        # If bash file was input, use that instead
        if len(sys.argv) == 2:
            client_bash = sys.argv[1]
        debug(main_logfile, '(main): client bash is ' + client_bash + '.')
        
        """
        bash = open(client_bash)
        ac_client = None
        for cmd in bash:
            cmd = cmd.strip()
            debug(main_logfile, '(main): cmd: ' + cmd)
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
        readline = ac_client.stdout.readline
        debug(main_logfile, '(main): Start parsing loop.')
        while True:
            next_line = readline()
            parseLine(next_line, screenshot_taken_queue, main_logfile)
            
    except IOError:
        debug(main_logfile, 'ERROR (main): ' + traceback.format_exc())
        print 'Could not find required file.'
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
                    debug(main_logfile, 'UNEXPECTED (main): ac_client.kill(): ' +
                          traceback.format_exc())
                    debug(main_logfile, 'UNEXPECTED (main): ac_client.returncode: ' +
                          str(ac_client.returncode))
                    break
        
        # Close the log file when no longer running
        # Make sure all upload threads are done
        # (Don't want to interrupt an upload)
        # TODO: add a backoff here + a message
        while screenshot_taken_queue.qsize() > 0:
            time.sleep(1)
        screenshot_taken_thread.stop()

        # imgur uploads are time consuming, so finish the current upload
        # and leave the rest for the next time jerboa is run
        imgur_upload_thread.stop()
        # Stay here until the screenshot_upload_queue has been updated
        while imgur_upload_thread.isAlive():
            time.sleep(1)
        
        while screenshot_uploaded_queue.qsize() > 0:
            time.sleep(1)
        screenshot_uploaded_thread.stop()
        
        while screenshot_taken_thread.isAlive() or screenshot_uploaded_thread.isAlive():
            time.sleep(1)
        
        main_logfile.close()

def parseConfigLine(line, logfile):
    """
    Parses each line from the jerboa config file (c.JERBOA_CONFIG_FILE)
    Saves config parameters in global variables
    Parameters:
        line - The line to parse
        logfile - The parser's logfile. Used for calls to 'debug()'.
    Returns:
        True on success, False on failure. Don't need to continue parsing
        after all config parameters are found.
    """
    global user_id
    global upload_key
    
    # Clean up input line
    line = line.strip()

    # Ignore empty lines
    if line == '':
        return

    # Config section:
    # // [JERBOA] DO NOT ALTER OR DELETE THIS COMMENT: 12 Art84j4a
    # // [JERBOA] DO NOT ALTER OR DELETE THIS COMMENT: <user id> <upload key>

    # Check for user info:
    groups = re.match('^\s*//\s*\[JERBOA\] DO NOT ALTER OR DELETE THIS COMMENT:\s+(\d+)\s+(.*)', line)
    if groups:
        user_id = groups.group(1)
        upload_key = groups.group(2)
        is_line_handled = True
        debug(logfile, line)
        debug(logfile, '(parseLine): parseConfigLine: ' + str(groups.groups()))
        return True
    else:
        return False
        
def parseLine(line, screenshot_taken_queue, logfile):
    """
    Parses each line from the ac_client output and enqueues screenshot
    representations in 'screenshots' for upload.
    Parameters:
        line - The line to parse
        screenshot_taken_queue - A limitless queue to buffer screenshot updates
        logfile - The parser's logfile. Used for calls to 'debug()'
    Returns:
        None
    """
    # Needed to maintain parsing state
    global ss_in_progress
    global ac_map
    global ac_mode
    global ac_mastermode
    global ac_ip
    global ac_port
    global ac_minutes_remaining
    global ac_players
    
    global blacklist
    global blacklist_reason
    global blacklist_name
    global blacklist_ip

    global most_recent_ss_name
    
    global user_id
    global upload_key
    
    # Used for debug logging
    is_line_handled = False
    
    # Clean up input line
    line = line.strip()

    # Ignore empty lines
    if line == '':
        return
        
    # Only parse everything else if config (id & key) have been found
    if user_id and upload_key:
        # Check for screenshot command:
        # Get screenshot url and add to screenshot_queue for upload
        # writing to file: F:\Documents\AssaultCube_v1.1\screenshots\20120601_22.56.13_ac_desert_TOSOK.jpg
        groups = re.match('^writing to file:\s+(.+\.(jpg|bmp))', line)
        if groups:
            if most_recent_ss_name == groups.group(1):
                return
            most_recent_ss_name = groups.group(1)
            ss_in_progress = True
            ac_players = []
            is_line_handled = True
            debug(logfile, line)
            debug(logfile, '(parseLine): Screenshot: ' + str(groups.groups()))
            
        # Get ac_minutes_remaining
        # gametimemaximum = 900000
        # gametimemaximum = <milliseconds of game length>
        groups = re.match('^minutesremaining\s+=\s+(\d+)', line)
        if groups:
            ac_minutes_remaining = int(groups.group(1))
            is_line_handled = True
            debug(logfile, line)
            debug(logfile, '(parseLine): minutesremaining: ' + str(groups.groups()))
            
        # Check for server info:
        groups = re.match('^\[jerboa\]server_info\s([^\s]+)\s(\d+)\s(\d+)\s?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?\s?(\d+)?', line)
        # Get map/mode and server details.
        # [jerboa]server_info ac_desert 7 0 64.85.165.123 28765
        # [jerboa]server_info <map> <mode id> <mastermode id> <server ip> <server port>
        if groups:
            ac_map = groups.group(1)
            ac_mode = groups.group(2)
            ac_mastermode = groups.group(3)
            ac_ip = "" if groups.group(4) == None else groups.group(4)
            ac_port = "" if groups.group(5) == None else groups.group(5)
            is_line_handled = True
            debug(logfile, line)
            debug(logfile, '(parseLine): [jerboa]server_info: ' + str(groups.groups()))

        # Get pstat_weap / pstat_score details.
        # [jerboa]pstat_info 0 0 0 0 0 0 HyPE|GDM 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        # [jerboa]pstat_info <cn> <flag> <frags> <deaths> <score> <team> <nick>
        # <knife_atk> <knife_dmg> <pistol_atk> <pistol_dmg> <carbine_atk> <carbine_dmg>
        # <shotgun_atk> <shotgun_dmg> <smg_atk> <smg_dmg> <sniper_atk> <sniper_dmg>
        # <assault_atk> <assault_dmg> <cpistol_atk> <cpistol_dmg> <nade_atk> <nade_dmg>
        # <akimbo_atk> <akimbo_dmg>
        groups = re.match('^\[jerboa\]pstat_info (\d+)\s(-?\d+)\s(-?\d+)\s(\d+)\s(-?\d+)\s(\d+)\s(.*)\s(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*', line)
        if groups:
            ac_players.append(groups.groups())
            is_line_handled = True
            debug(logfile, line)
            debug(logfile, '(parseLine): pstat_info: ' + str(groups.groups()))

        # Check for blacklist
        # [jerboa]blacklist reason: cheating cheater
        groups = re.match('^\[jerboa\]blacklist reason:\s+(.*)$', line)
        if groups:
            blacklist_reason = groups.group(1).strip()
            blacklist = True
            is_line_handled = True
            debug(logfile, line)
            debug(logfile, '(parseLine): blacklist: ' + str(groups.groups()))

        # Only check /whois if blacklist procedure started
        if blacklist:
            # Get user name
            # name   HyPE|GDM
            groups = re.match('^name\s+(.*)$', line)
            if groups:
                blacklist_name = groups.group(1).strip()
                is_line_handled = True
                debug(logfile, line)
                debug(logfile, '(parseLine): blacklist name: ' +
                      str(groups.groups()))

            # Get user ip
            # IP    127.0.0.1
            groups = re.match('^IP\s+(.*)$', line)
            if groups:
                blacklist_ip = groups.group(1).strip()
                is_line_handled = True
                debug(logfile, line)
                debug(logfile, '(parseLine): blacklist IP: ' +
                      str(groups.groups()))
        
        # Check for procedure end signal and add to screenshot_queue for upload
        # 
        groups = re.match('^\[jerboa\]complete', line)
        if groups and ss_in_progress:
            # TODO: mildly inefficient
            screenshot = ScreenshotData(most_recent_ss_name, user_id,
                                        upload_key, ac_map, ac_mode,
                                        ac_mastermode, ac_ip, ac_port,
                                        ac_minutes_remaining, ac_players)
            if blacklist:
                screenshot = BlacklistScreenshotData(most_recent_ss_name, user_id,
                                                     upload_key, ac_map, ac_mode,
                                                     ac_mastermode, ac_ip, ac_port,
                                                     ac_minutes_remaining,
                                                     ac_players,
                                                     blacklist_name, blacklist_ip,
                                                     blacklist_reason,
                                                     blacklist_name + ' blacklist',
                                                     blacklist_reason, 'blacklist')
            screenshot_taken_queue.put(screenshot, True)
            ss_in_progress = False
            ac_players = []
            blacklist = False
            is_line_handled = True
            debug(logfile, line)
            debug(logfile, '(parseLine): ' + most_recent_ss_name + ' procedure complete: ' + str(time.time()))

    # Debug
    if not is_line_handled:
        debug(logfile, line)
        pass
        
if __name__ == '__main__':
    main()
