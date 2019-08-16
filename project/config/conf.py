# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    '''
    base config
    '''
    APP_NAME = 'flaskframe'

    SECRET_KEY = os.environ.get('SECRET_KEY') or b']\xe5\x18\x1euE\x9c\x05\xd8\x8f\x91\xba\xb9\xbd\xf0\xd65\x85j\xf3\xe4\xaa\xc3+'
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