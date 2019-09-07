# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-15
@function:
init flask app
'''
import os
import logging
from flask import Flask, request
from flask_compress import Compress
from werkzeug.contrib.fixers import ProxyFix
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.conf import setconfig
from utils.logger import initLogger
from utils.send_email import set_emailsetting


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30/minute", "300/hour", "3000/day"],
    headers_enabled=True  # X-RateLimit写入响应头。
)

from app import helloapi


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


def init_utils(app):
    # init email
    set_emailsetting(app.logger, app.config['APP_NAME'])


def create_app():
    ## 初始化app
    app = Flask(__name__)
    Compress(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # 初始化配置文件
    conf_name =  os.environ.get('RUN_ENV') or 'default'
    app.config.from_object(setconfig[conf_name])

    limiter.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response


    # 初始化app日志
    init_app_logger(app)
    init_utils(app)

    # 初始化api
    app.register_blueprint(helloapi, url_prefix='/hello')

    return app