#!/usr/bin/env python

import logging
import functools


def logged(func):
    @functools.wraps(func)
    def with_logging(*args, **kwargs):
        s_args = ", ".join(map(str, args))
        s_kwargs = ", ".join("%s=%s" % kwarg for kwarg in kwargs.items())
        logging.debug("Calling %s(%s, %s)", func.__name__, s_args, s_kwargs)
        retval = func(*args, **kwargs)
        logging.debug("Returning %s(%s, %s) = %s", func.__name__, s_args, s_kwargs, retval)
        return retval
    return with_logging
