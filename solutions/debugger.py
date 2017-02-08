import datetime as dt
from functools import wraps


def log_method(func, cls, name, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start = dt.datetime.now()
            func(*args, **kwargs)
        finally:
            end = dt.datetime.now()
            Debugger.method_calls.append({
                'class': type(args[0]),
                'method': name,
                'args': args,
                'kwargs': kwargs,
                'time': (end - start),
            })
    return wrapper


def log_attr_get(func, cls):
    @wraps(func)
    def wrapper(self, name):
        try:
            value = object.__getattribute__(self, name)
            return value
        finally:
            Debugger.attribute_accesses.append({
                'action': 'get',
                'class': type(self),
                'attribute': name,
                'value': value
            })
    return wrapper


def log_attr_set(func, cls):
    @wraps(func)
    def wrapper(self, name, value):
        try:
            object.__setattr__(self, name, value)
        finally:
            Debugger.attribute_accesses.append({
                'action': 'set',
                'class': type(self),
                'attribute': name,
                'value': value
            })
    return wrapper


class Meta(type):
    def __new__(cls, name, parents, dct):
        for attr, item in dct.items():
            if callable(item):
                dct[attr] = log_method(item, cls, attr)
        dct['__getattribute__'] = log_attr_get(object.__getattribute__, cls)
        dct['__setattr__'] = log_attr_set(object.__setattr__, cls)
        return type.__new__(cls, name, parents, dct)


class Debugger:
    method_calls = []
    attribute_accesses = []
