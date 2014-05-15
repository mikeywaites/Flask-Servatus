#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
import shutil
import tempfile

from cStringIO import StringIO

from flask import Flask

from .. import Servatus
from ..storages import FileSystemStorage
from ..exceptions import SuspiciousFileOperation

servatus = Servatus()


def factory():

    app = Flask(__name__)
    app.config['SERVATUS_MEDIA_ROOT'] = 'media_dir'
    servatus.init_app(app)

    return app


class FileSystemStorageTests(unittest.TestCase):

    storage_class = FileSystemStorage

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.app = factory()

        with self.app.app_context():
            self.storage = self.storage_class(location=self.temp_dir,
                                              base_url='/test_media_url/')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_file_with_path(self):

        self.storage.save('path/to/test.file', StringIO('This is a file'))
        self.assertTrue(os.path.exists(
                        os.path.join(self.temp_dir, 'path', 'to', 'test.file')))

    def test_file_exists(self):

        self.storage.save('test.file', StringIO('This is a file'))
        self.assertTrue(self.storage.exists('test.file'))

    def test_file_path(self):

        self.assertEqual(self.storage.path('test.file'),
                         os.path.join(self.temp_dir, 'test.file'))

    def test_delete_file(self):

        self.storage.save('test.file', StringIO('This is a file'))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'test.file')))

        self.storage.delete('test.file')
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'test.file')))

    def test_file_storage_prevents_directory_traversal(self):
        self.assertRaises(SuspiciousFileOperation, self.storage.exists, '../')
        self.assertRaises(SuspiciousFileOperation, self.storage.exists, '/etc/passwd')

    def test_file_url(self):

        self.assertEqual(self.storage.url('test.file'),
                         '%s%s' % (self.storage.base_url, 'test.file'))
