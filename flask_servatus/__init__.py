#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app

from werkzeug.local import LocalProxy

from .utils import get_storage_class


class Servatus(object):

    def __init__(self, app=None, storage=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        app.config.setdefault('SERVATUS_MEDIA_ROOT', '')
        app.config.setdefault('SERVATUS_MEDIA_URL', '/media/')
        app.config.setdefault('SERVATUS_STORAGE_CLASS',
                              'flask_servatus.storages.FileSystemStorage')
        app.config.setdefault('SERVATUS_UPLOAD_DIR_PERMISSIONS', None)
        app.config.setdefault('SERVATUS_FILE_UPLOAD_PERMISSIONS', None)

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['servatus'] = self

    def get_storage_class(self):

        return get_storage_class(current_app.config['SERVATUS_STORAGE_CLASS'])


get_default_storage = LocalProxy(lambda: _get_servatus())


def _get_servatus():
    """return the currently configured servatus instance attached to
    `current_app`.

    """

    return current_app.extensions['servatus']
