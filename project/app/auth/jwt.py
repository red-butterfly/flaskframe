# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-15
@function:
for user to jwt
'''

import datetime
import time
import jwt
from functools import wraps
from flask import jsonify, request
from config.conf import Config
from utils.responseInfo import response_normal, response_error


class Auth():

    @staticmethod
    def authenticate(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'iss': Config.APP_NAME,
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def _decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False})

            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = (400, '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self._decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    ##TODO 获取用户信息
                    user = ['user': 'hanfei', 'login_time': 123]
                    if (user is None):
                        result =(400, '找不到该用户信息')
                    else:
                        if (user['login_time'] == payload['data']['login_time']):
                            result = (200, '请求成功')
                        else:
                            result = (400, 'Token已更改，请重新登录获取')
                else:
                    result = (400, payload)
        else:
            result = (400, '没有提供认证token')
        return result

    def jwt_identify(self):
        '''
        jwt鉴权认证的装饰器
        :param ParamFormat: 验证字符串的格式
        :return:
        '''
        def wrapper(func):
            @wraps(func)
            def decorator(*args, **kwargs):
                # 首先进行数据正确性验证
                status, message = self.identify(request)

                if status != 200:
                    return response_error(status, message)
                # 运行 route 函数
                return func(*args, **kwargs)
            return decorator
        return wrapper