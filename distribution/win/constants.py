"""
constants.py
This file contains constants used by jerboa.py

Copyright 2012, gdm
"""

# Toggles debug logging
IS_DEBUG = True
# Toggles testing (read from saved log files) mode
IS_TESTING = False
IS_TESTING_CHECK_CREDITS = False
IS_TESTING_SINGLE_IMAGE = True
DEFAULT_TEST_FILE = 'clientlog.txt'

APPLICATION_NAME = 'Jerboa AssaultCube Client Wrapper'
APPLICATION_VERSION = '1.1.0.4.1'

ASSAULTCUBE_VERSION = '1.1.0.4'
EXIT_RETRY_INTERVAL = 1
NT_OS_NAME = 'nt'
NT_DEFAULT_BASH_FILE = 'assaultcube.bat'
POSIX_OS_NAME = 'posix'
POSIX_DEFAULT_BASH_FILE = 'assaultcube.bat'
CONFIG_FILE = 'config/autoexec.cfg'

# Debug logging parameters
LOG_DIR = 'jerboa_logs'
LOGFILE_PREFIX = 'jerboa_log_'
LOGFILE_SUFFIX = '.txt'

# Imgur
IMGUR_API_KEY = '475add36e0e43bd3d3c4510fd436e8e2'
IMGUR_UPLOAD_URL = 'http://api.imgur.com/2/upload.json'

# Jerboa's RESTful urls
GET_UNSENT_SCREENSHOTS_URL = 'http://hype-clan.com/jerbo_a/restful_api/get_unsent_screenshots.php'
TAKEN_SCREENSHOT_URL = 'http://hype-clan.com/jerbo_a/restful_api/taken_screenshot.php'
UPLOADED_SCREENSHOT_URL = 'http://hype-clan.com/jerbo_a/restful_api/uploaded_screenshot.php'
##GET_UNSENT_SCREENSHOTS_URL = 'http://localhost/jerboa/scratch/restful_api/get_unsent_screenshots.php'
##TAKEN_SCREENSHOT_URL = 'http://localhost/jerboa/scratch/restful_api/taken_screenshot.php'
##UPLOADED_SCREENSHOT_URL = 'http://localhost/jerboa/scratch/restful_api/uploaded_screenshot.php'

# POST intervals (seconds)
# '1' should be the minimum UPDATE_INTERVAL
# AC saves to timestamp-named image files, so if you take multiple screenshots
# within 1 second, only the last one will be saved (others will be overwritten)
UPDATE_INTERVAL = 1
UPDATE_BACKOFF_INCREMENT = 5
MAX_UPDATE_BACKOFF = 60
