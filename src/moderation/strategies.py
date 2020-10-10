import functools
import operator
import random

_RESET = object()

def _advance_once(func):
    @functools.wraps(func)
    def ret_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        next(ret)
        return ret
    return ret_func

@_advance_once
def fibonacci():
    got = yield None
    while True:
        a, b = 0, 1 
        while got is _RESET:
            got = yield None
        yield a
        while True:                                                        
            if (got := (yield b)) is _RESET:
                break   
            a, b = b, a + b

@_advance_once
def exponential(base):
    got = yield None
    value = 1
    while True:
        while got is _RESET:
            value = 1
            got = yield None
        got = yield value
        value *= base

@_advance_once
def linear():
    got = yield None
    value = 0
    while True:
        while got is _RESET:
            value = 0
            got = yield None
        got = yield value
        value += 1

def transform(generator, *transformers):
    @_advance_once
    def inner():
        sent = yield None
        while True:
            value = generator.send(sent)
            if value is not None:
                for transformer in transformers:
                    value = transformer(value)
            sent = yield value
    return inner()
    
def scale(factor):
    return functools.partial(operator.mul, factor)

def power(exponent):
    return lambda value: value ** exponent
 
def cap(limit):
    return functools.partial(min, limit)

def at_least(limit):
    return functools.partial(max, limit)
    
def jitter(min_value=0.9, max_value=1.1):
    def ret_value(value):
        return value * random.uniform(min_value, max_value)
    return ret_value

def reset(generator):
    generator.send(_RESET)
    
def qt(generator, *, factor=1, upper_limit=float("+inf"), lower_limit=0, min_jitter=0.9, max_jitter=1.1):
    return transform(generator, scale(factor), cap(upper_limit), 
                     at_least(lower_limit), jitter(min_value=min_jitter, max_value=max_jitter))
