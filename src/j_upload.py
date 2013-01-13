"""
logger.py
This file contains classes and methods used by jerboa.py
- post()

- AbstractUploadThread

Copyright 2013, gdm
"""

# TODO: get rid of the config import?
import j_config as c
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
    logger.debug('(post): url = ' + url)
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
        
    def handle_response(self, element, post_response):
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
                        self.logger.debug(self.log_identifier + ': POST RESPONSE: ' +
                                          str(post_response))
                        successful_post = self.handle_response(element,
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
