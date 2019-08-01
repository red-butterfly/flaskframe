# -*- coding: utf-8 -*-
'''
mysql的对象
created by HanFei on 19/2/28
'''
import os
import threading
import MySQLdb
from utils.parse_dburi import parse_db_str


class MySQLDB(object):
    
    _instance_lock = threading.Lock()
    _instance = {}

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if args[0] not in cls._instance:
                cls._instance[args[0]] = super(MySQLDB, cls).__new__(cls)
        return cls._instance[args[0]]

    def __init__(self, mysql_uri):
        print(os.environ.get(mysql_uri))
        mysql_config = parse_db_str(os.environ.get(mysql_uri))
        self.db = MySQLdb.connect(
            host = mysql_config['host'],
            user = mysql_config['user'],
            passwd = mysql_config['passwd'],
            db = mysql_config['db']
        )
        self.cursor = self.db.cursor()
    
    def get_db(self):
        return (self.db, self.cursor)
        

class MySQLBase(object):

    _db_uri = 'MYSQL_URI'

    def __init__(self):
        self.db, self.cursor = MySQLDB(self._db_uri).get_db()


class OAccount(MySQLBase):

    def __init__(self):
        super(OAccount, self).__init__()
        self.field_list = {
        }

    def get_agt_user(self):
        self.cursor.execute(
            'SELECT user_id,app_secret FROM agt_user WHERE user_type in (1,2)'
        )

        return self.cursor.fetchall()