"""
parser.py
This file contains classes and methods used by jerboa.py
- Config
- BasicScreenshotData
- ScreenshotData
- BlacklistScreenshotData

- Parser

Copyright 2013, gdm
"""

# TODO: get rid of the config import?
import j_config as c
import re
import time
import traceback

class BasicScreenshotData(object):
    def __init__(self, local_file_path, user_id, upload_key):
        self.local_file_path = local_file_path
        self.user_id = user_id
        self.upload_key = upload_key
        self.imgur_hash = ''
        self.imgur_delete_hash = ''
        # Some metrics to report to Jerboa
        # self.imgur_attempt_count = 0

class ScreenshotData(BasicScreenshotData):
    def __init__(self, local_file_path, user_id, upload_key, ac_map, ac_mode,
                 ac_mastermode, ac_ip, ac_port, ac_minutes_remaining,
                 ac_players, title = 'title', caption = 'caption', tags = ''):
        super(ScreenshotData, self).__init__(local_file_path,
                                             user_id, upload_key)
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

class BlacklistScreenshotData(ScreenshotData):
    def __init__(self, local_file_path, user_id, upload_key, ac_map, ac_mode,
                 ac_mastermode, ac_ip, ac_port, ac_minutes_remaining,
                 ac_players, name, ip, reason, title = 'title',
                 caption = 'caption', tags = ''):
        super(BlacklistScreenshotData, self).__init__(
            local_file_path, user_id, upload_key, ac_map, ac_mode,
            ac_mastermode, ac_ip, ac_port, ac_minutes_remaining, ac_players,
            title, caption, tags)
        self.name = name
        self.ip = ip
        self.reason = reason

class Config():
    """
    Config is a simple wrapper for user-specific parameters (usually read in
    from a config file in the user's AC client directory)
    """

    def __init__(self, user_id, upload_key):
        """
        Parameters:
            user_id = user's id in Jerboa's database
            upload_key = user's secret upload key in Jerboa's database
        """
        self.user_id = user_id
        self.upload_key = upload_key
    
    def complete(self):
        return self.user_id != None and self.upload_key != None



class Parser():
    def __init__(self, logger):
        self.logger = logger
        self.config = Config(None, None)
        # Needed to maintain parsing state.
        self.ss_in_progress = False
        self.ac_map = 'unknown'
        self.ac_mode = '0'
        self.ac_mastermode = '0'
        self.ac_ip = ''
        self.ac_port = ''
        self.ac_minutes_remaining = 0
        self.ac_players = []

        self.blacklist = False
        self.blacklist_reason = 'reason'
        self.blacklist_name = 'name'
        self.blacklist_ip = '127.0.0.1'

        self.most_recent_ss_name = ''


    def loadConfig(self, configfile_name):
        self.logger.debug('(Parser.loadConfig): Jerboa config: ' +
                          configfile_name)
        try:
            config_file = open(configfile_name, 'r')
            for line in config_file:
                self.logger.debug('(Parser.loadConfig): config_file line: ' +
                                  line)
                self.parseConfigLine(line)
                if self.config.complete():
                    break
        except:
            self.logger.debug('(Parser.loadConfig): ERROR unexpected: ' +
                              traceback.format_exc())
            raise
            

    def parseConfigLine(self, line):
        """
        Parses each line from the jerboa config file
        Parameters:
            line - <string> The line to parse
        Returns:
            Updates 'self.config'
        """
        # Clean up input line
        line = line.strip()

        # Ignore empty lines
        if line != '':

            self.logger.debug(line)

            # Sample config section:
            # // [<log name>] DO NOT ALTER OR DELETE THIS COMMENT: 12 Art84j4a
            # // [<log name>]] DO NOT ALTER OR DELETE THIS COMMENT: <user id> <upload key>

            # Check for user's config parameters:
            groups = re.match('^\s*//\s*\[' + c.LOG_NAME +'\] DO NOT ALTER OR DELETE THIS COMMENT:\s+(\d+)\s+(.*)', line)
            if groups:
                self.config.user_id = groups.group(1)
                self.config.upload_key = groups.group(2)
                self.logger.debug('(Parser.parseConfigLine): ' +
                                  str(groups.groups()))
    
    def reset(self):
        self.ss_in_progress = False
        self.ac_players = []
        self.blacklist = False

    def parseLine(self, line, screenshot_taken_queue):
        """
        Parses each line from the AC client output and enqueues screenshot
        representations in 'screenshots' for upload.
        Parameters:
            line - <string> The line to parse
            screenshot_taken_queue - <Queue.Queue> For buffering screenshot updates
            self.logger - <self.logger> self.logger
        Returns:
            Updates state
        """
        
        # Clean up input line
        line = line.strip()

        # Ignore empty lines
        if line == '':
            return

        self.logger.debug(line)
        
        # Check for screenshot command:
        # Get screenshot url and add to screenshot_queue for upload
        # writing to file: F:\Documents\AssaultCube_v1.1\screenshots\20120601_22.56.13_ac_desert_TOSOK.jpg
        groups = re.match('^writing to file:\s+(.+\.(jpg|bmp))', line)
        if groups:
            if self.most_recent_ss_name == groups.group(1):
                return
            self.most_recent_ss_name = groups.group(1)
            self.ss_in_progress = True
            self.ac_players = []
            self.logger.debug('(Parser.parseLine): Screenshot: ' +
                              str(groups.groups()))
            
        # Get self.ac_minutes_remaining
        # gametimemaximum = 900000
        # gametimemaximum = <milliseconds of game length>
        groups = re.match('^minutesremaining\s+=\s+(\d+)', line)
        if groups:
            self.ac_minutes_remaining = int(groups.group(1))
            self.logger.debug('(Parser.parseLine): minutesremaining: ' +
                              str(groups.groups()))
            
        # Check for server info:
        groups = re.match('^\[' + c.LOG_NAME +'\]server_info\s([^\s]+)\s(\d+)\s(\d+)\s?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?\s?(\d+)?', line)
        # Get map/mode and server details.
        # [jerboa]server_info ac_desert 7 0 64.85.165.123 28765
        # [jerboa]server_info <map> <mode id> <mastermode id> <server ip> <server port>
        if groups:
            self.ac_map = groups.group(1)
            self.ac_mode = groups.group(2)
            self.ac_mastermode = groups.group(3)
            self.ac_ip = "" if groups.group(4) == None else groups.group(4)
            self.ac_port = "" if groups.group(5) == None else groups.group(5)
            self.logger.debug('(Parser.parseLine): [jerboa]server_info: ' +
                              str(groups.groups()))

        # Get pstat_weap / pstat_score details.
        # [jerboa]pstat_info 0 0 0 0 0 0 HyPE|GDM 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        # [jerboa]pstat_info <cn> <flag> <frags> <deaths> <score> <team> <nick>
        # <knife_atk> <knife_dmg> <pistol_atk> <pistol_dmg> <carbine_atk> <carbine_dmg>
        # <shotgun_atk> <shotgun_dmg> <smg_atk> <smg_dmg> <sniper_atk> <sniper_dmg>
        # <assault_atk> <assault_dmg> <cpistol_atk> <cpistol_dmg> <nade_atk> <nade_dmg>
        # <akimbo_atk> <akimbo_dmg>
        groups = re.match('^\[' + c.LOG_NAME +'\]pstat_info (\d+)\s(-?\d+)\s(-?\d+)\s(\d+)\s(-?\d+)\s(\d+)\s(.*)\s(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*', line)
        if groups:
            self.ac_players.append(groups.groups())
            self.logger.debug('(Parser.parseLine): pstat_info: ' +
                              str(groups.groups()))

        # Check for self.blacklist
        # [jerboa]self.blacklist reason: cheating cheater
        groups = re.match('^\[' + c.LOG_NAME +'\]self.blacklist reason:\s+(.*)$', line)
        if groups:
            self.blacklist_reason = groups.group(1).strip()
            self.blacklist = True
            self.logger.debug('(Parser.parseLine): self.blacklist: ' +
                              str(groups.groups()))

        # Only check /whois if self.blacklist procedure started
        if self.blacklist:
            # Get user name
            # name   HyPE|GDM
            groups = re.match('^name\s+(.*)$', line)
            if groups:
                self.blacklist_name = groups.group(1).strip()
                self.logger.debug('(Parser.parseLine): self.blacklist name: ' +
                                  str(groups.groups()))

            # Get user ip
            # IP    127.0.0.1
            groups = re.match('^IP\s+(.*)$', line)
            if groups:
                self.blacklist_ip = groups.group(1).strip()
                self.logger.debug('(Parser.parseLine): self.blacklist IP: ' +
                                  str(groups.groups()))
        
        # Check for procedure end signal and add screenshot to screenshot_queue
        # for upload
        groups = re.match('^\[' + c.LOG_NAME +'\]complete', line)
        if groups and self.ss_in_progress:
            # TODO: mildly inefficient
            screenshot = ScreenshotData(self.most_recent_ss_name,
                                        self.config.user_id,
                                        self.config.upload_key, self.ac_map,
                                        self.ac_mode, self.ac_mastermode,
                                        self.ac_ip, self.ac_port,
                                        self.ac_minutes_remaining,
                                        self.ac_players)
            if self.blacklist:
                screenshot = self.blacklistScreenshotData(
                    self.most_recent_ss_name, self.config.user_id,
                    self.config.upload_key, self.ac_map, self.ac_mode,
                    self.ac_mastermode, self.ac_ip, self.ac_port,
                    self.ac_minutes_remaining,
                    self.ac_players,
                    self.blacklist_name, self.blacklist_ip,
                    self.blacklist_reason,
                    self.blacklist_name + ' self.blacklist',
                    self.blacklist_reason, 'self.blacklist')
            self.logger.debug('(Parser.parseLine): Right before push ' + screenshot.local_file_path);
            screenshot_taken_queue.put(screenshot, True)
            self.logger.debug('(Parser.parseLine): Pushed ' + screenshot.local_file_path + ' into queue!');
            self.reset()
            self.logger.debug('(Parser.parseLine): ' +
                              self.most_recent_ss_name +
                              ' procedure complete: ' + str(time.time()))
