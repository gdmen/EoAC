 if c.IS_TESTING:
            if c.IS_TESTING_CHECK_CREDITS:
                json_handle = post('http://api.imgur.com/2/credits.json',
                   {'key' : c.IMGUR_API_KEY},
                   main_logfile)
            elif c.IS_TESTING_SINGLE_IMAGE:
                with open("F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120603_16.15.07_ac_desert_TOSOK.jpg", "rb") as image_file:
                    base64encoded = base64.b64encode(image_file.read())
        
                debug(main_logfile, 'base64: ' + base64encoded)
                json_handle = post(c.IMGUR_UPLOAD_URL,
                       {'key' : c.IMGUR_API_KEY,
                        'image' : base64encoded,
                        'type' : 'base64',
                        'title' : 'title',
                        'caption' : 'caption'},
                       main_logfile)
                imgur_json = json.loads(json_handle.read())
                debug(main_logfile, 'JSON RESPONSE: ' + str(imgur_json))
                if 'error' in imgur_json:
                    debug(main_logfile, 'JSON RESPONSE ERROR.')
                elif 'upload' in imgur_json:
                    debug(main_logfile, 'JSON RESPONSE SUCCESS.')
                main_logfile.close()
                sys.exit()
            else:           
                # Set the default test log file
                test_file_name = c.DEFAULT_TEST_FILE
                test_file = open(test_file_name)
                print c.APPLICATION_NAME + " running"
                print "Ctrl-C to exit"
                for line in test_file:
                    parseLine(line, screenshot_queue, main_logfile)
                    #raw_input("Press Enter to continue...")
                print 'Finishing uploads, please wait . . .'
                test_file.close()
                # Close the log file when no longer running
                # Make sure screenshot_thread is done
                # (Don't want to interrupt an upload)
                # TODO: add a backoff here + a message
                while screenshot_queue.qsize() > 0:
                    time.sleep(1)
                screenshot_thread.running = False
                while screenshot_thread.isAlive():
                    time.sleep(1)
                screenshot_thread.stop()
                main_logfile.close()
