# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-15
@function:
flask 的view文件
'''
import logging

from flask import Blueprint
from flask import jsonify
from flask import current_app
from flask import request

from utils.send_email import send_email
from utils.simple_async import async_submit
from config.conf import Config
from database.mongo_model import TestClass
from init_app import limiter


logger = logging.getLogger(Config.APP_NAME)
helloapi = Blueprint('helloapi', __name__)


@helloapi.route('/world', methods=['GET'])
@limiter.limit("2/minute;5/hour")
def index():
    logger.error('start!!!!!!!!!!!')
    # async_submit(
    #     send_email, 'debug from hello', 'this is to test send email for debug info!', [request.url]
    # )
    logger.error('end!!!!!!!!!!!')
    return jsonify({'msg': 'hello world'})