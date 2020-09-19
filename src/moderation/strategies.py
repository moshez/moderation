_RESET = object()

def fibonacci():
    while True:
        a, b = 0, 1
        if (yield a) is _RESET:
            yield 0
            continue
        while True:
            if (yield b) is _RESET:
                yield 0
                break
            a, b = b, a + b

def exponential(base):
    value = 1
    while True:
        if (yield value) is _RESET:
            value = 1
        else:
            value *= base

def linear():
    value = 1
    while True:
        if (yield value) is _RESET:
            value = 0
        else:
            value += 1

def transform(generator, *transformers):
    def inner():
        sent = yield 0
        while True:
            value = generator.send(sent)
            for transformer in transformers:
                value = transformer(value)
            sent = yield value
    ret_value = inner()
    next(ret_value)
    return ret_value
    
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
