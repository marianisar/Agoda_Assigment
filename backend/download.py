#!/usr/bin/python3
#############################################################################
#                                                                           #
#                       Copyright 2020 Maria Nisar.                         #
#                           All Rights Reserved.                            #
#                                                                           #
# THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY INFORMATION WHICH IS THE  #
#                   PROPERTY OF Maria Nisar                                 #
#                                                                           #
#############################################################################
'''
Module to Download Files.
@author: Maria Nisar
'''
import os
import sys
import ssl
import time
import logging
import argparse
import configparser
from logging import handlers
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import urlopen
from multiprocessing.dummy import Pool

import mysql.connector
from databse import Database

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


class Downloader(object):

    def __init__(self):
        """
        Initialize object.
        @return: None (none)
        """
        self.logger = self.get_rsyslogger('Agoda')
        self.dbconn = None
        self.download_path = None
        self.size = None
        self.max_time = None
        self.read_settings()

    def read_settings(self):
        """
        Read from config and set value of instances.
        @return : None.
        """
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(curr_dir, 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_file)
        cdb_conf = 'Database Server Configuration'
        main_dbconn = {'host':     config.get(cdb_conf, 'SERVER_ADDR'),
                       'user':     config.get(cdb_conf, 'SERVER_USER'),
                       'passwd':   config.get(cdb_conf, 'SERVER_PASS'),
                       'db':       config.get(cdb_conf, 'DATABASE'),
                       'use_pure': False}
        self.dbconn = Database(logger=self.logger, **main_dbconn)
        self.download_path = config.get('Download Path', 'download_location')
        cnf = 'Download Configuration'
        self.size = config.getint(cnf, 'max_size')
        self.max_time = config.getint(cnf, 'max_time')
        self.validate_downloads_path()

    def validate_downloads_path(self):
        """
        @return: None
        """
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def connect_to_db(self, terminate=True):
        """
        Make a connection to DB or exit.
        @param terminate: If true exit with error code 1. (boolean)
        @return: True if connected else False or exit. (none)
        """
        try:
            self.dbconn.connect()
            return True
        except mysql.connector.Error as exce:
            self.logger.error(str(exce))
            if terminate:
                sys.exit(1)
            return False

    def save_file(self, data):
        """
        write meta data of file to DB.
        @param data: list of file data. (object)
        @return: True if batch processed successfully else False. (boolean)
        """
        self.connect_to_db()
        tablename = 'data'
        try:
            self.logger.info('Saving Data into Database')
            self.dbconn.conn.autocommit = False
            for metadata in data:
                if not metadata:
                    continue
                self.dbconn.write_to_db(metadata, tablename)
                self.logger.info('Data saved successfully')
            self.dbconn.conn.autocommit = True
            return True
        except mysql.connector.Error as exce:
            self.logger.error('Error while saving data')
            self.logger.error(exce)
            self.dbconn.conn.autocommit = True
            return False

    def download_files(self, url, tries=3, wait=3):
        """
        Download file and save its meta data into database
        @param url: Url to download file. (string)
        @param tries: Number of tries before giving up on connection. (int)
        @param wait: Wait before next attempt. (int)
        @return: data dict of url . (dict)
        """
        filename = os.path.join(self.download_path, url.split('/')[-1])
        if os.path.exists(filename):
            self.logger.info('File %s already exist :', filename)
            return None
        failures = 0
        file_size = 0
        start_time = datetime.now()
        s_time = int(time.time())
        for attempt in range(tries + 1):
            try:
                self.logger.info('Downloading start of : %s', filename)
                # Start downloading
                open_url = urlopen(url, context=CTX)
                with open(filename, 'wb') as file:
                    while True:
                        chunk = open_url.read(8192)
                        if not chunk:
                            break
                        file_size += len(chunk)
                        file.write(chunk)
                    break
            except Exception as exce:
                if attempt < tries:
                    failures += 25
                    file_size = 0
                    self.logger.warning(str(exce))
                    msg = 'Attempt # %d failed, retrying in %d seconds.'
                    self.logger.warning(msg, attempt, wait)
                    time.sleep(wait)
                else:
                    self.logger.warning(str(exce))
                    os.remove(filename)
                    self.logger.error(exce)
                    data = {
                        'file_source':        url,
                        'file_destination':   filename,
                        'start_time':         start_time,
                        'end_time':           datetime.now(),
                        'protocol':           urlparse(url).scheme,
                        'data_type':          'Not downloaded',
                        'download_speed':     'Slow',
                        'failure_percentage': '100',
                        'status':             'Downloading Failed'
                    }
                    return data
        # Validate downloaded file
        self.logger.info('validating downloaded file ...')
        if os.path.getsize(filename) == file_size:
            self.logger.info('%s : File downloaded', filename)
            data_type = 'large' if file_size > self.size else 'small'
            s_time = int(time.time()) - s_time
            speed = 'Slow' if s_time > self.max_time else 'Fast'
            status = 'Download complete'
        else:
            os.remove(filename)
            self.logger.warning('Incomplete download, file removed.')
            data_type = 'Not downloaded'
            speed = 'Slow'
            failures = '100'
            status = 'Downloading Failed'
        data = {
            'file_source':        url,
            'file_destination':   filename,
            'start_time':         start_time,
            'end_time':           datetime.now(),
            'protocol':           urlparse(url).scheme,
            'data_type':          data_type,
            'download_speed':     speed,
            'failure_percentage': failures,
            'status':             status
        }
        return data

    def get_rsyslogger(self, name, level=logging.INFO, log_format=None):
        """
        Get the logger object with watched file handler.
        This will check if the file has changed in logrotate.
        @param name: Name for the logger. (string)
        @param level: Debug level. (int)
        @param log_format: Logging format. (string)
        @return: Logger object. (instance)
        """
        logger = logging.getLogger(name=name)
        logger.setLevel(level)

        syslog_handler = handlers.SysLogHandler(address='/dev/log')
        if log_format is None:
            log_format = ('%(asctime)s %(name)s[%(process)d] : '
                          '<%(levelname)s> %(message)s')
        formatter = logging.Formatter(log_format, '%b %d %I:%M:%S')
        syslog_handler.setFormatter(formatter)
        syslog_handler.setLevel(level)

        if logger.handlers:
            logger.handlers = []

        logger.addHandler(syslog_handler)
        return logger


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    # Received urls arguments.
    PARSER.add_argument('-u', '--urls', nargs='+', help='<Required> URLS',
                        required=True, dest='urls')
    # Parse arguments.
    ARGS = PARSER.parse_args()
    URLS = ARGS.urls
    # Create class object.
    DOWN = Downloader()
    WORKERS = 8
    # Create polls.
    POOL = Pool(WORKERS)
    # Download files in poll.
    DATA = POOL.map(DOWN.download_files, URLS)
    POOL.close()
    # wait for all threats.
    POOL.join()
    # Save files into Database.
    DOWN.save_file(DATA)
