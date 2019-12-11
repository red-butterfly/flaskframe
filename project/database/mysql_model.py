# -*- coding: utf-8 -*-
'''
mysql的对象
created by HanFei on 19/2/28
'''
import os
import threading
import MySQLdb
from utils.parse_dburi import parse_db_str
from utils.tools import dict_obj_to_str


class MySQLDB(object):
    
    _instance_lock = threading.Lock()
    _instance = {}
    _firstinit = {}

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if args[0] not in cls._instance:
                cls._instance[args[0]] = super(MySQLDB, cls).__new__(cls)
        return cls._instance[args[0]]

    def __init__(self, mysql_uri):
        if mysql_uri not in MySQLDB._firstinit:
            mysql_config = parse_db_str(os.environ.get(mysql_uri))
            self.__pool = PooledDB(
                creator=MySQLdb, mincached=1, maxcached=20,
                host=mysql_config['host'], port=mysql_config['port'], user=mysql_config['user'],
                passwd=mysql_config['passwd'],
                db=mysql_config['db'], use_unicode=False, charset='utf8', 
                cursorclass=DictCursor
            )
            
            MySQLDB._firstinit[mysql_uri] = True
    
    def get_db(self):
        db = self.__pool.connection()
        return (db, db.cursor())
        

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

        oa_list = []
        for result in self.cursor.fetchall():
            json = dict_obj_to_str(result)
            oa_list.append(json)

        return oa_list