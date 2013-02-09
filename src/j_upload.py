"""
logger.py
This file contains classes and methods used by jerboa.py
- post()

- AbstractUploadThread

Copyright 2013, gdm
"""

# TODO: get rid of the config import?
import j_config as c
from j_parser import BasicScreenshotData, ScreenshotData, BlacklistScreenshotData
import base64
import json
import os
import Queue
import threading
import time
import traceback
import urllib


def post(url, params, logger):
    """
    Http POSTs 'params' to 'url'
    Expects 'params' in a map formatted like:
        {name(string):value(string)}
    Returns:
        Result on success
        False on failure
    """
    logger.debug('(post): url = ' + url.split('/')[-1])
    try:
        for key, value in params.items():
            params[key] = str(value)
            logger.debug('(post): ' + key + ' = ' + params[key][:32])
        logger.debug('(post): ' + urllib.urlencode(params))
        return urllib.urlopen(url, urllib.urlencode(params))
    except IOError, e:
        logger.debug('ERROR (post): ' + traceback.format_exc())
        print 'Failed to connect to the ' + c.APPLICATION_NAME + ' server.'
        print 'Retrying . . .'
        return False
    except:
        logger.debug('ERROR UNEXPECTED (post): ' + traceback.format_exc())
        raise


class AbstractUploadThread(threading.Thread):
    """
    AbstractUploadThread is not meant to be instantiated.
    AbstractUploadThread POSTs elements from a given 'in_queue' to a given
    'upload_url'.
    On succesive <c.STATS_UPDATE_INTERVAL> intervals:
        Pulls a new element from the in_queue and POSTs the parameters to
        the upload_url.
        If POST fails, pushes element back on top of the queue.
        Linear back off on successive failures.
    """
    def __init__(self, in_queue, upload_url, log_identifier, logger):
        self.in_queue = in_queue
        self.upload_url = upload_url
        self.log_identifier = log_identifier
        self.running = True
        # b_ are backoff variables
        # The run method's loop always sleeps for c.UPDATE_INTERVAL, but the
        # backoff procedure alters the number of loops made before action.
        # e.g. if b_post_interval is 20, the run loop will loops 20 times with no
        # action other than sleeping for c.UPDATE_INTERVAL
        # This allows for faster (graceful) stoppe of the thread and is a bit
        # cleaner than saving and comparing times between posts
        self.b_counter = 0
        self.b_last_post = 0
        self.b_post_interval = 1
        self.logger = logger
        threading.Thread.__init__(self)
    
    def backoff(self):
        if self.b_post_interval <= (c.MAX_UPDATE_BACKOFF -
                                    c.UPDATE_BACKOFF_INCREMENT):
            self.b_post_interval += c.UPDATE_BACKOFF_INCREMENT
        self.logger.debug('(' + self.log_identifier +
              '.backoff): new interval = '
              + str(self.b_post_interval) + ' seconds')
        
    def posterize(self, element):
        """
        Converts the input element to the corresponding dictionary of POST
        parameters
        """
        raise NotImplementedError("Should have implemented this")
        
    def handleResponse(self, element, post_response):
        """
        Handles the response from POST.
        Returns TRUE on expected response, FALSE to trigger a retry
        """
        raise NotImplementedError("Should have implemented this")
        
    def stop(self):
        self.running = False
    
    def run(self):
        while self.running:
            time.sleep(c.UPDATE_INTERVAL)
            try:
                self.b_counter += 1
                if self.b_counter - self.b_last_post >= self.b_post_interval:
                    self.b_last_post = self.b_counter
                    # Get the next element to POST
                    # get_nowait() throws an empty queue exception - this is
                    # caught and ignored (if it blocks here, we may not be able
                    # to end this thread gracefully)
                    element = self.in_queue.get_nowait()

                    # Flag to know if upload was successful
                    # i.e. if element should be put back in queue
                    successful_post = True

                    post_response = post(self.upload_url,
                                         self.posterize(element),
                                         self.logger)
                    # If POST failed to connect to server
                    if post_response == False:
                        successful_post = False
                        self.logger.debug(self.log_identifier + ': POST FALSE')
                    else:
                        post_response = post_response.read()
                        self.logger.debug(self.log_identifier + ': POST TRUE')
                        self.logger.debug(self.log_identifier +
                                          ': POST RESPONSE: ' +
                                          str(post_response))
                        successful_post = self.handleResponse(element,
                                                               post_response)
                                                
                    self.logger.debug(self.log_identifier + ': queue size: ' +
                          str(self.in_queue.qsize()))

                    if not successful_post:
                        # If POST failed for any reason, put element back into
                        # queue and increase the backoff time
                        self.in_queue.put(element, True)
                        self.backoff()
                        self.logger.debug('(' + self.log_identifier +
                              '.run) backing off.')
            except Queue.Empty:
                # Want to loop rather than blocking for the queue, so ignore
                # this
                continue
            except:
                self.logger.debug(self.log_identifier + 'ERROR unexpected: ' +
                      traceback.format_exc())
                raise


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
                        prnt = ('Uploading ' + str(num_uploads) +
                               ' prior image')
                        if num_uploads != 1:
                            prnt += 's'
                        prnt += '. . .'
                        self.logger.debug(prnt, True)
                    for local_file_path in local_file_paths_json:
                        self.logger.debug('(' + self.log_identifier + '.run): '
                                          + 'FILE PATH: ' + local_file_path)
                        try:
                            with open(local_file_path) as ss:                               
                                screenshot = BasicScreenshotData(
                                                local_file_path,
                                                self.config.user_id,
                                                self.config.upload_key)
                                self.imgur_queue.put(screenshot, True)
                        except IOError as e:
                            self.logger.debug('(' + self.log_identifier +
                                              '.run): ' + 'FILE DNE: ' +
                                              local_file_path)
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
                      'user_version' : c.APPLICATION_VERSION,
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
        
    def handleResponse(self, screenshot, post_response):
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
            self.logger.debug('Saved metadata: ' +
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
        
    def handleResponse(self, screenshot, post_response):
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
        
    def handleResponse(self, screenshot, post_response):
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
            self.logger.debug('Uploaded image: ' +
                      str(os.path.basename(screenshot.local_file_path)), True)
            return True
