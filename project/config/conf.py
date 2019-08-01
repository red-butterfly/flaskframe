# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    '''
    base config
    '''
    APP_NAME = 'flaskframe'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Yf\x82\x07A\x9d\xb0\xe2\x93\x8aH?M\x83\xcf\xda\xf6\xa5\xc9\xf7\xcb%2^'
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOGFILE_PATH = os.path.join(os.environ.get('HOST_PATH'), 'log') if os.environ.get('HOST_PATH') else '/var/log'


class DevConfig(Config):
    '''
    development env
    '''
    pass


class ProductConfig(Config):
    '''
    product env
    '''
    pass


setconfig = {
    'dev': DevConfig,
    'pro': ProductConfig,
    'default': DevConfig
}