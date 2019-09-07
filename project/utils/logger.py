# -*- coding: utf-8 -*-
'''
created by hanfei on 17/8/29
'''
import logging
from logging.handlers import TimedRotatingFileHandler


_logger_level = {
    'fatal': logging.FATAL,
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}


def initLogger(name ,filename, log_level="INFO", when='W6', interval=1, backupCount=30,
               format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'):
    '''
    "S"：Second 秒; "M"：Minutes 分钟; "H"：Hour 小时; "D"：Days 天;"W"：Week day（0 = Monday）
    :param name:
    :param filename:
    :param log_level:
    :param when:
    :param interval:
    :param backupCount:
    :param format:
    :return:
    '''
    # 默认的日志为 INFO，各模块的输出日志等级在 params中定义：(DEBUG/INFO/WARNING/ERROR/CRITICAL
    logging.basicConfig(level=log_level, format=format)
    handler = TimedRotatingFileHandler(filename, when, interval, backupCount)
    handler.suffix = "%Y-%m-%d.log"
    handler.setLevel(log_level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)


def initLogger_flask(filename, log_level="INFO", when='W6', interval=5, backupCount=30,
               format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'):
    '''
    针对flask，只返回handler
        "S"：Second 秒; "M"：Minutes 分钟; "H"：Hour 小时; "D"：Days 天;"W"：Week day（0 = Monday）
        :param name:
        :param filename:
        :param log_level:
        :param when:
        :param interval:
        :param backupCount:
        :param format:
        :return:
    '''
    # 默认的日志为 INFO，各模块的输出日志等级在 params中定义：(DEBUG/INFO/WARNING/ERROR/CRITICAL
    logging.basicConfig(level=log_level, format=format)
    handler = TimedRotatingFileHandler(filename, when, interval, backupCount)
    handler.setLevel(log_level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    return handler
