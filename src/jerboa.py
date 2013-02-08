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


def versionCheck(config, logger):
    """
    Http POSTs to the application server and checks current version.
    If out of date, prompts for update and exits.
    *This method is blocking.*
    Parameters:
        config = Config object from j_parser
        logger = Logger object from j_logger
    """
    log_identifier = 'versionCheck'
    successful_post = False
    while not successful_post:
        post_response = post(c.VERSION_CHECK_URL,
                             {'user_id' : config.user_id,
                              'upload_key' : config.upload_key,
                              'user_version' : c.APPLICATION_VERSION},
                             logger)
        if post_response == False:
            continue

        post_response = post_response.read()
        logger.debug('POST RESPONSE: ' + str(post_response))

        if len(post_response) > 0:
            logger.debug('('  + log_identifier + '): VERSION CHECK ERROR: ' +
                              str(post_response))
            return False
        return True

    
def main():
    """
    Script's entry point.
    """
    print c.APPLICATION_NAME + ' version ' + c.APPLICATION_VERSION

    is_debug = c.IS_DEBUG
    if len(sys.argv) > 4:
        print "That's too many command line args!"
        if os.name == c.POSIX_OS_NAME:
            print '> ./' + c.FILE_NAME_NIX +' -d'
            print '> ./' + c.FILE_NAME_NIX +' -c <custom config>'
        elif os.name == c.NT_OS_NAME:
            print '> ' + c.FILE_NAME_WIN +' -d'
            print '> ' + c.FILE_NAME_WIN +' -c <custom config>'
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
                print '> ./' + c.FILE_NAME_NIX +' -c <custom config>'
            elif os.name == c.NT_OS_NAME:
                print '> ' + c.FILE_NAME_WIN +' -d'
                print '> ' + c.FILE_NAME_WIN +' -c <custom config>'
        logger.close()
        raw_input("Press Enter to Quit")
        return

    try:
        threads_initiated = False
        # Instantiate Parser
        parser = Parser(logger)
        # If config file was specified by user, use that instead
        # Might throw an IndexError
        client_config = c.CONFIG_FILE
        if len(sys.argv) >= 3 and '-c' in sys.argv:
            client_config = sys.argv[sys.argv.index('-c') + 1]
            print "Using specified config file (" + client_config + ")."
        # Read in configuration parameters
        parser.loadConfig(client_config)

        # Die if config parameters were not all there
        if not parser.config.complete():
            logger.debug('(main): ' + client_config + ' missing parameters.')
            print 'ERROR: missing configuration parameter in ' + client_config
            logger.close()
            raw_input("Press Enter to Quit")
            return
    
        # Version check
        if not versionCheck(parser.config, logger):
            logger.debug('**You must download the latest version of ' + c.APPLICATION_NAME + '**', True)
            return

        logger.debug(' (main): Version check success!')

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
                print '> ./' + c.FILE_NAME_NIX +' -c <custom config>'
            elif os.name == c.NT_OS_NAME:
                print '> ' + c.FILE_NAME_WIN +' -d'
                print '> ' + c.FILE_NAME_WIN +' -c <custom config>'
        print '. . .'
        if threads_initiated:
          get_unsent_screenshots_thread.stop()
          screenshot_taken_thread.stop()
          imgur_upload_thread.stop()
          screenshot_uploaded_thread.stop()
        logger.close(True)
        raw_input("Press Enter to Quit")
        return

    #ac_client_started = False
    #ac_client = None
    try:
        ac_client = subprocess.Popen(client_bash,
                                     shell = False,
                                     stdin = subprocess.PIPE,
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.STDOUT)
        ac_client_started = True
        # Avoid having to re-interpret dot notation in the loop
        ac_readline = ac_client.stdout.readline
        logger.debug('(main): Start parsing loop.')
        while True:
            line = ac_readline()
            if not line or ac_client.poll() != None:
                raise KeyboardInterrupt()
            ac_client.stdin.write('\n')
            ac_client.stdin.flush()
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
                print '> ./' + c.FILE_NAME_NIX +' -c <custom config>'
            elif os.name == c.NT_OS_NAME:
                print '> ' + c.FILE_NAME_WIN +' -d'
                print '> ' + c.FILE_NAME_WIN +' -c <custom config>'
        print '. . .'
        get_unsent_screenshots_thread.stop()
        screenshot_taken_thread.stop()
        imgur_upload_thread.stop()
        screenshot_uploaded_thread.stop()
        logger.close(True)
        raw_input("Press Enter to Quit")
        return
    except KeyboardInterrupt:
        try:
            logger.debug('KeyboardInterrupt (main)')
            
            logger.debug('\nSaving screenshot metadata, DO NOT EXIT.', True)

            # If windows client was started and is still running
            if  os.name == c.NT_OS_NAME and ac_client_started and ac_client.poll() == None:
                ac_client.send_signal(signal.CTRL_C_EVENT)
                ac_client.send_signal(signal.CTRL_C_EVENT)
                while not ac_client.returncode:
                    try:
                        ac_client.kill()
                        time.sleep(0.05)
                    except:
                        logger.debug('UNEXPECTED (main): ac_client.kill(): ' +
                                     traceback.format_exc())
                        logger.debug('CLIENT EXITED FIRST (main): ac_client.returncode: ' +
                                     str(ac_client.returncode))
                        break
            
            # Make sure we get any remaining output chilling in the subprocess's
            # output pipe
            while True:
                line = ac_readline()
                if not line:
                  break
                parser.parseLine(line, screenshot_taken_in_queue)
            ac_client.stdout.close()

            remaining_uploads = (screenshot_taken_in_queue.qsize() +
                              imgur_upload_in_queue.qsize() +
                              screenshot_uploaded_in_queue.qsize())
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
                time.sleep(0.25)
            screenshot_taken_thread.stop()
            while screenshot_taken_thread.isAlive():
                time.sleep(0.25)
            logger.debug('\n**It is now safe to exit. All screenshot metadata saved.**\n',
                       True)
            # Finish all imgur uploads (could be time consuming!)
            while imgur_upload_in_queue.qsize() > 0:
                time.sleep(0.25)
            imgur_upload_thread.stop()
            while imgur_upload_thread.isAlive():
                time.sleep(0.25)

            # Finish all application website updates
            while screenshot_uploaded_in_queue.qsize() > 0:
                time.sleep(0.25)
            screenshot_uploaded_thread.stop()
            while screenshot_uploaded_thread.isAlive():
                time.sleep(0.25)

            while (screenshot_taken_thread.isAlive() or
                   imgur_upload_thread.isAlive() or
                   screenshot_uploaded_thread.isAlive()):
                time.sleep(0.25)
        except KeyboardInterrupt:
            get_unsent_screenshots_thread.stop()
            screenshot_taken_thread.stop()
            imgur_upload_thread.stop()
            screenshot_uploaded_thread.stop()
        finally:
            get_unsent_screenshots_thread.stop()
            screenshot_taken_thread.stop()
            imgur_upload_thread.stop()
            screenshot_uploaded_thread.stop()
            logger.close(True)

        
if __name__ == '__main__':
    main()
