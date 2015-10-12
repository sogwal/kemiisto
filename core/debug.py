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
        logging.debug("Returning %s(%s, %s) = %s",
                      func.__name__, s_args, s_kwargs, retval)
        return retval
    return with_logging

# https://zapier.com/engineering/profiling-python-boss/

import time


class Profiling():
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name=''):
        print '{timer} {checkpoint} took {elapsed} seconds'.format(
            timer=self.name,
            checkpoint=name,
            elapsed=self.elapsed,
        ).strip()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
