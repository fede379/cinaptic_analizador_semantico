from operator import methodcaller
import re
import os
import argparse

def concat_arrays(arrays):
    result = []
    for i, arr in enumerate(arrays):
        for i, ar1 in enumerate(arr):
            result.append(ar1)

    return result

def parse_string(s):
    return "_".join(filter(lambda x: x is not "", map(methodcaller("strip"), s.strip().split(" ")))).capitalize()

def check_string(value):    
    ivalue = str(value).strip()
    regex = re.compile('^([a-zA-Z ]+)+$')
    if not regex.match(ivalue):
        raise argparse.ArgumentTypeError(
            "%s is an invalid string value" % value)
    return ivalue

def check_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                "%s must be a positive integer" % value)
        return ivalue
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            "%s must be a positive integer" % value)

def is_path_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)

def check_path(value):
    try:
        ivalue = str(value)
        if not is_path_creatable(ivalue):
            raise argparse.ArgumentTypeError(
                "%s must be a valid creatable path (check file permissions)" % value)
        return ivalue
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            "%s must be a valid creatable path (check file permissions)" % value)