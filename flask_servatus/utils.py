# -*- coding: utf-8 -*-
"""
    flask_servatus.utils
    ---------------

    Provides a collection of utils used throughout `flask_servatus`

"""

import importlib

from itertools import chain


def load_class(full_class_string):
    """ dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)


def get_storage_class(storage_class):
    """return a storage class loaded from a python module string

    Ex::
        >>> get_storage_class('faster.foo.bar.S3Storage')

    :raises: AttributeError, ImportError
    :returns: storage class
    """
    storage = load_class(storage_class)
    return storage


def tuple_from(*iters):
    return tuple(chain(*iters))


def extension(filename):
    return filename.rsplit('.', 1)[-1]


def lowercase_ext(filename):
    if '.' in filename:
        main, ext = filename.rsplit('.', 1)
        return main + '.' + ext.lower()
    else:
        return filename.lower()


def addslash(url):
    if url.endswith('/'):
        return url
    return url + '/'
