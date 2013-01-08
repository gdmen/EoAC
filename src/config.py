"""
config.py
This file contains constants used by jerboa.py

Copyright 2013, gdm
"""

# Toggles debug logging
IS_DEBUG = True
# Debug logging parameters
LOG_DIR = 'jerboa_logs'
LOGFILE_PREFIX = 'jerboa_log_'
LOGFILE_SUFFIX = '.txt'

#HOST_URL = 'http://hype-clan.com/jerbo_a'
HOST_URL = 'http://localhost/jerboa_website'

APPLICATION_NAME = 'Jerboa AssaultCube Client Wrapper'
ASSAULTCUBE_VERSION = '1.1.0.4'
APPLICATION_VERSION = ASSAULTCUBE_VERSION + '.2'

# Exiting procedure timeout
EXIT_RETRY_INTERVAL = 1
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
GET_UNSENT_SCREENSHOTS_URL = HOST_URL + '/restful_api/get_unsent_screenshots.php'
TAKEN_SCREENSHOT_URL = HOST_URL + '/restful_api/taken_screenshot.php'
UPLOADED_SCREENSHOT_URL = HOST_URL + '/restful_api/uploaded_screenshot.php'

# POST intervals (seconds)
# '1' should be the minimum UPDATE_INTERVAL
# AC saves to timestamp-named image files, so if you take multiple screenshots
# within 1 second, only the last one will be saved (others will be overwritten)
UPDATE_INTERVAL = 1
UPDATE_BACKOFF_INCREMENT = 5
MAX_UPDATE_BACKOFF = 60
