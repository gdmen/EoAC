
class ImgurUploadThread(threading.Thread):
    """
    ImgurUploadThread uploads screenshots to Imgur and then update the Jerboa
    server with the links.
    On succesive <c.STATS_UPDATE_INTERVAL> intervals:
        Pulls a new screenshot from the imgur_upload_queue and posts the image
        to Imgur.
        If post fails, pushes screenshot back on top of the queue.
        Backs off on successive failures.
    """
    def __init__(self, queue, logfile):
        self.queue = queue
        self.running = True
        # b_ are backoff variables
        self.b_counter = 0
        self.b_last_post = 0
        self.b_post_freq = 1
        self.logfile = logfile
        threading.Thread.__init__(self)
    def backoff(self):
        if self.b_post_freq < c.MAX_UPDATE_BACKOFF:
            self.b_post_freq += c.UPDATE_BACKOFF_INCREMENT
        debug(self.logfile, '(EventUpdateThread.run): backing off; new interval = '
              + str(self.b_post_freq) + ' seconds')
    def run(self):
        while self.running:
            time.sleep(c.UPDATE_INTERVAL)
            try:
                self.b_counter += 1
                if self.b_counter - self.b_last_post >= self.b_post_freq:
                    # Get the next ScreenshotData object
                    # get_nowait() throws an empty queue exception - this is
                    # caught and ignored
                    ss_data = self.queue.get_nowait()

                    # Set up array for post to Jerboa website
                    screenshot_array = {'key' : ss_data.key,
                                        'user_id' : ss_data.user_id,
                                        'imgur_hash' : ss_data.imgur_hash,
                                        'imgur_delete_hash' : ss_data.imgur_delete_hash,
                                        'ac_server' : ss_data.ac_server,
                                        'ac_map' : ss_data.ac_map,
                                        'ac_mode' : ss_data.ac_mode,
                                        'title' : ss_data.title,
                                        'caption' : ss_data.caption,
                                        'tags' : ss_data.tags}
        
                    # TODO: Perhaps find a more extensible way of handling this
                    if isinstance(ss_data, BlacklistScreenshotData):
                        screenshot_array['blacklist_name'] = ss_data.name
                        screenshot_array['blacklist_ip'] = ss_data.ip

                    # Flag to know if imgur upload was successful
                    # i.e. if it is okay to update Jerboa
                    successful_posts = True
                    
                    # If not already uploaded to Imgur:
                    if ss_data.imgur_hash == '' and ss_data.imgur_delete_hash == '':
                        # Convert to base64 and upload to Imgur
                        source = open(ss_data.local_file_path, 'rb')
                        debug(self.logfile, 'ss_data.local_file_path: ' + ss_data.local_file_path)
                        ss_encoded_base64 = base64.b64encode(source.read())
                        debug(self.logfile, 'base64: ' + ss_encoded_base64)

                        json_handle = post(c.IMGUR_UPLOAD_URL,
                                           {'key' : c.IMGUR_API_KEY,
                                            'image' : ss_encoded_base64,
                                            'title' : ss_data.title,
                                            'caption' : ss_data.caption},
                                           self.logfile)
                        # TODO:
                        # > I hope we get have received all the json by this time o.O
                        # > Not sure if the unicode strings from this will be problematic
                        if json_handle == False:
                            debug(self.logfile, 'Post failed: ' + ss_data.local_file_path)
                            ss_data.imgur_attempt_count += 1
                            successful_posts = False
                        else:
                            imgur_json = json.loads(json_handle.read())
                            debug(self.logfile, 'JSON RESPONSE: ' + str(imgur_json))

                            # I was going to check for 'not imgur_json', but that's true for
                            # empty lists, and so, I assume it might be for empty json as well
                            if imgur_json == None or 'error' in imgur_json:
                                debug(self.logfile, 'JSON RESPONSE ERROR.')
                                ss_data.imgur_attempt_count += 1
                                successful_posts = False
                            elif 'upload' in imgur_json:
                                debug(self.logfile, 'JSON RESPONSE SUCCESS.')
                                debug(self.logfile, '(ScreenshotUploadThread.run): ' +
                                      ss_data.local_file_path + ' to imgur: ' + str(time.time()))
                                # Save the imgur hashes in case post to the Jerboa server fails
                                ss_data.imgur_hash = imgur_json['upload']['image']['hash']
                                ss_data.imgur_delete_hash = imgur_json['upload']['image']['deletehash']
                                # Update screenshot data
                                screenshot_array['imgur_hash'] = ss_data.imgur_hash
                                screenshot_array['imgur_delete_hash'] = ss_data.imgur_delete_hash
                            
                        debug(self.logfile, 'Screenshots queue size: ' + str(self.queue.qsize()))

                    # Jerboa update (only if Imgur update was successful)
                    if successful_posts and post(c.REPORT_SCREENSHOT_URL,
                                                 screenshot_array,
                                                 self.logfile):
                        # If post was successful, update 'b_last_post' number and
                        # reset post frequency to 1
                        self.b_last_post = self.b_counter
                        self.b_post_freq = 1
                        debug(self.logfile, '(ScreenshotUploadThread.run) SUCCESSFUL Jerboa post: ' + ss_data.local_file_path)
                        debug(self.logfile, '(ScreenshotUploadThread.run): ' +
                                      ss_data.local_file_path + ' to Jerboa: ' + str(time.time()))
                    else:
                        successful_posts = False
                        debug(self.logfile, '(ScreenshotUploadThread.run) FAILED Jerboa post: ' + ss_data.local_file_path)
                        
                    if not successful_posts:
                        # If either post failed to connect to web server, put event back
                        # into queue and increase the backoff time
                        self.queue.put(ss_data, True)
                        self.backoff()
                        debug(self.logfile, '(ScreenshotUploadThread.run) backing off: ' +ss_data.local_file_path)
            except Queue.Empty:
                continue
            except:
                debug(self.logfile,
                      'ERROR (ScreenshotUploadThread.run) unexpected: ' +
                      traceback.format_exc())
                raise
        # Close the log file when no longer running
        self.logfile.close()
        
    def stop(self):
        self.running = False
