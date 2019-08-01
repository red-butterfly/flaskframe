# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-15
@function:
function for init flask
'''
import os
import logging

from utils.logger import initLogger
from utils.send_email import set_emailsetting
from app import helloapi


_logger_level = {
    'fatal': logging.FATAL,
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}


def init_app_logger(app):
    '''
    init the app's logger
    :param app:
    :return:
    '''
    if not os.path.exists(app.config['LOGFILE_PATH']):
        try:
            os.makedirs(app.config['LOGFILE_PATH'])
        except FileExistsError as e:
            print('file exist')

    # handler = initLogger_flask(os.path.join(app.config['LOGFILE_PATH'], app.config['APP_NAME']))
    # app.logger.addHandler(handler)
    # app.logger.setLevel(_logger_level[app.config['LOG_LEVEL']])
    initLogger(app.config['APP_NAME'], os.path.join(app.config['LOGFILE_PATH'], app.config['APP_NAME']))


def init_blueprint(app):
    app.register_blueprint(helloapi, url_prefix='/hello')


def init_utils(app):
    # init email
    set_emailsetting(app.logger, app.config['APP_NAME'])