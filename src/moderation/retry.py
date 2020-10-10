import functools
import time

from moderation import strategies


def retry(backoff, sleeper=time.sleep, exceptions=(), retries=3):
    exceptions = tuple(exceptions)

    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries - 1):
                try:
                    ret_value = func(*args, **kwargs)
                except exceptions:
                    sleeper(next(backoff))
                else:
                    break
            else:
                try:
                    ret_value = func(*args, **kwargs)
                except exceptions:
                    raise
            strategies.reset(backoff)
            return ret_value

        return wrapper

    return real_decorator
