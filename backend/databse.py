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
import time
import mysql.connector as MySQLdb
import snxpyutils.helpers as h


class Database(object):
    '''
    A Database class to instantiate a database object.
    '''

    CEXT = MySQLdb.HAVE_CEXT
    ERROR = MySQLdb.Error

    def __init__(self, **kwargs):
        '''
        Initialize a database object, agoda is default database.
        @return: None (none)
        '''
        # MySQL Configuration
        self.dsn = kwargs
        self.dsn.setdefault('host', 'localhost')
        self.dsn.setdefault('user', 'agoda')
        self.dsn.setdefault('passwd', 'Snx@D3fault')
        self.dsn.setdefault('db', 'download')
        self.dsn.setdefault('connect_timeout', 30)
        try:
            self.prepared = self.dsn.pop('prepared')
        except KeyError:
            self.prepared = None
        try:
            self.dictionary = self.dsn.pop('dictionary')
        except KeyError:
            self.dictionary = None
        # MySQL Handle
        self.conn = None
        self.cursor = None
        self.logger = h.pop(kwargs, 'logger', h.get_rsyslogger('SNX-DB'))

    def connect(self, tries=3, wait=3):
        '''
        Start connection to database with given number tries and wait.
        @param tries: Number of tries before giving up on connection. (int)
        @param wait: Wait before next attempt. (int)
        @return: None. (none)
        @raise mysql.connector.Error: If connection fails.
        '''
        if self.conn is not None:
            try:
                self.conn.ping(True)
            except MySQLdb.Error as exce:
                msg = '%s, unable to connect to DB.'
                self.logger.error(msg, str(exce))
                raise exce
            return None

        for attempt in range(1, tries + 1):
            try:
                self.conn = MySQLdb.connect(autocommit=True, **self.dsn)
            except (self.ERROR, Exception) as exc:
                # Retry if MySQL service is not running
                if attempt < tries:
                    self.logger.warning(str(exc))
                    msg = 'Attempt # %d failed, retrying in %d seconds.'
                    self.logger.warning(msg, attempt, wait)
                    time.sleep(wait)
                else:
                    self.logger.warning(str(exc))
                    msg = 'Attempt # %d failed as well.'
                    self.logger.warning(msg, attempt)
                    msg = 'Unable to connect to DB after %d attempts.'
                    self.logger.error(msg, attempt)
                    raise exc
            else:
                self.cursor = self.conn.cursor(dictionary=self.dictionary,
                                               prepared=self.prepared)
                break
        return None

    def __del__(self):
        '''
        Close the connection on application termination.
        @return None. (none)
        '''
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def executemany(self, query, params=None):
        '''
        Executes a batch of queries (suitable for batch insertions).
        @param query: SQL query to be executed. (string)
        @param params: List of tuples of query parameters. (list)
        @return None. (none)
        '''
        # params = [
        # ('Jane', 1),
        # ('Joe', 22),
        # ('John', 9),
        # ]
        if self.cursor is not None:
            self.cursor.executemany(operation=query, seq_params=params)

    def close(self):
        '''
        Close connection with mconsole database.
        @return None. (none)
        '''
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def write_to_db(self, data, table):
        '''
        Write list of given data to the database.
        @param data: Data dict(s) to insert. (list)
        @param table: Table name where insert will be made. (string)
        @return: None. (none)
        @note: No prior data with same primary key should exist.
        '''
        if not data:
            return None
        if isinstance(data, dict):
            data = [data]
        args = ", ".join(["%s"] * len(data[0]))
        columns = "`%s`" % '`,`'.join(data[0].keys())
        query = "INSERT INTO `{0}` ({1}) VALUES ({2});"
        query = query.format(table, columns, args)
        return self.executemany(query, [tuple(x.values()) for x in data])
