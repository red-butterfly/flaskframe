# -*- coding: utf-8 -*-
'''
Mongo的对象
created by HanFei on 19/2/28
'''
import os
import threading
import datetime
import copy
from pymongo import MongoClient
from utils.tools import datetime2str
from utils.parse_dburi import parse_db_str


class MongoDB(object):
    
    _instance_lock = threading.Lock()
    _instance = {}

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if args[0] not in cls._instance:
                cls._instance[args[0]] = super(MongoDB, cls).__new__(cls)
        return cls._instance[args[0]]

    def __init__(self, mongo_uri):
        if not mongo_uri:
            print('Can\'t get the MongolUri: {0}'.format(mongo_uri))
        self.mc = MongoClient(os.environ.get(mongo_uri), maxPoolSize=2000)
        mongo_config = parse_db_str(os.environ.get(mongo_uri))
        self.db = self.mc.get_database(mongo_config['db'])
    
    def get_db(self):
        return self.db


class MongoDBCollection(object):

    _db_uri = 'CIC_MONGO_URI'
    _collection = None

    def __init__(self):
        self.db = MongoDB(self._db_uri).get_db()
        
        if self._collection:
            self.coll = self.db[self._collection]


class TestClass(MongoDBCollection):

    def __init__(self):
        super(TestClass, self).__init__()
        self.field_list = {
        }

    def create_or_update(self, data: dict):
        pass
        # self.coll.find(filter=s_filter)
        # self.coll.update_many(s_filter, {"$set":data})
        # self.coll.insert_one(udata)
