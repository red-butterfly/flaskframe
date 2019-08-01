# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-15
@function:
init flask app
'''
import os

from flask import Flask
from flask_compress import Compress
from werkzeug.contrib.fixers import ProxyFix
from config.conf import setconfig
from .init_function import init_app_logger, init_blueprint, init_utils


## 初始化app
app = Flask(__name__)
Compress(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

# 初始化配置文件
conf_name = os.environ.get('RUN_ENV') or 'default'
app.config.from_object(setconfig[conf_name])


# 初始化app日志
init_app_logger(app)
init_blueprint(app)
init_utils(app)