# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-18
@function:
sample async
'''
import os
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=(os.cpu_count() or 1) * 4)


def async_submit(run_func, *args, **kwargs):
    '''
    submit the worker
    :param run_func:
    :param params:
    :return:
    '''
    executor.submit(run_func, *args, **kwargs)