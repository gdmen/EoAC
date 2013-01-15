"""
config.py
This file contains constants used by jerboa.py

Copyright 2013, gdm
"""
###############################################################################
# Annoying, but these params must be manually kept up to date along with the
# params in website/j_config.py
APP_NAME = "Eye of AC"
# To be clear, this 'LOG_NAME' is for parsing cubescript output
LOG_NAME = "EoAC"
FILE_NAME_WIN = "eoac.exe"
FILE_NAME_NIX = "eoac"
###############################################################################

# Toggles debug logging
IS_DEBUG = False
# Debug logging parameters
LOG_DIR = LOG_NAME + '_logs'
LOGFILE_PREFIX = LOG_NAME + '_log_'
LOGFILE_SUFFIX = '.txt'

HOST_URL = 'http://hype-clan.com/jerbo_a/restful_api/'
#HOST_URL = 'http://localhost/jerboa_website/restful_api/'

APPLICATION_NAME = 'EoAC'
ASSAULTCUBE_VERSION = '1.1.0.4'
APPLICATION_VERSION = ASSAULTCUBE_VERSION + '.3'

# Exiting procedure timeout
EXIT_RETRY_INTERVAL = 0.01
# NT ~= Windows
NT_OS_NAME = 'nt'
NT_DEFAULT_BASH_FILE = 'assaultcube.bat'
# POSIX ~= Linux
POSIX_OS_NAME = 'posix'
POSIX_DEFAULT_BASH_FILE = 'assaultcube.sh'
CONFIG_FILE = 'config/autoexec.cfg'

# Imgur
IMGUR_API_KEY = '475add36e0e43bd3d3c4510fd436e8e2'
IMGUR_UPLOAD_URL = 'http://api.imgur.com/2/upload.json'

# Jerboa's RESTful urls
GET_UNSENT_SCREENSHOTS_URL = HOST_URL + 'get_unsent_screenshots.php'
TAKEN_SCREENSHOT_URL = HOST_URL + 'taken_screenshot.php'
UPLOADED_SCREENSHOT_URL = HOST_URL + 'uploaded_screenshot.php'

# POST intervals (seconds)
# '1' should be the minimum UPDATE_INTERVAL
# AC saves to timestamp-named image files, so if you take multiple screenshots
# within 1 second, only the last one will be saved (others will be overwritten)
UPDATE_INTERVAL = 1
UPDATE_BACKOFF_INCREMENT = 5
MAX_UPDATE_BACKOFF = 60
