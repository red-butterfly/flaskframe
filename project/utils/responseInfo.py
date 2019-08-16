# -*- coding: utf-8 -*-
'''
对外接口的统一格式
created by HanFei on 19/2/28
'''
import json
from flask import request, jsonify
from functools import wraps


class RequsetDecorator():

    def __init__(self):
        self.checkList = ['query', 'header', 'body-data', 'body-form', 'file']

    def _check_param(self, param_list):
        inputs = {}

        for param_type in param_list:
            if param_type not in inputs:
                inputs[param_type] = {}
            if param_type in ['query', 'header', 'body-form']:
                for key, ktype, kdefault in param_list[param_type]:
                    if param_type == 'query':
                        getparam = request.args.get(key, kdefault)
                    elif param_type == 'header':
                        getparam = request.headers.get(key, kdefault)
                    elif param_type == 'body-form':
                        getparam = request.form.get(key, kdefault)
                    try:
                        inputs[param_type][key] = int(getparam) if getparam and ktype == 'int' else getparam
                    except Exception as e:
                        return False, 'Error: {0}({1}) is {2} , data type {3}}'.format(
                                key, ktype, param_type, e
                            )
            
            elif param_type == 'body-data':
                if param_list[param_type] == 'json':
                    try:
                        inputs[param_type] = json.loads(request.get_data(as_text=True))
                    except:
                        return False, 'Error: {0} data get error'.format(param_type)

            elif param_type == 'file':
                for fname in param_list[param_type]:
                    if fname not in request.files:
                        return False, 'Error: not upload file <{0}>!'.format(fname)
                    file = request.files[fname]
                    if file and file.filename == '':
                        return False, 'Error: No selected file <{0}>!'.format(fname)
                    inputs[param_type][fname] = file
        
        return True, inputs

    def check(self, logger, req_param):
        '''
        {'query': (), 'header': (), 'data': (), 'form': (), 'file': []}
        请求授权的装饰器，以及验证数据
        暂时不做必要参数检测
        :param ParamFormat: 验证字符串的格式
        :return:
        '''
        def wrapper(func):
            @wraps(func)
            def decorator(*args, **kwargs):
                # 首先进行数据正确性验证
                inputs = {}

                param_list = req_param[request.method]
                status, result = self._check_param(param_list)

                if not status:
                    logger.error(result)
                    return response_error(400, result)

                logger.info('[{method}] {path} | input: {param}'.format(
                    method = request.method, 
                    path = request.path, 
                    param = json.dumps({key:value for key, value in result.items() if key != 'file'}))
                )

                if 'file' in param_list:
                    logger.info('Files: {0}'.format(json.dumps([ file.filename for _,file in inputs['file'].items()])))
                # 运行 route 函数
                return func(result, *args, **kwargs)
            return decorator
        return wrapper


def response_error(code, errmsg):
    '''
    出错的返回格式
    :param errmsg:
    :return:
    '''
    #return abort(406,errmsg)
    return jsonify({'errcode':code,'errmsg':errmsg,'data':None})


def response_normal(code, result):
    '''
    正常的信息的返回格式
    :param result:
    :return:
    '''
    return jsonify({'errcode':code,'errmsg':None,'data':result})


ReqDec = RequsetDecorator()