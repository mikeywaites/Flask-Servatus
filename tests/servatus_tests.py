import unittest

from flask import Flask

from .. import Servatus
from ..storages import FileSystemStorage

servatus = Servatus()


def factory():

    app = Flask(__name__)
    app.config['SERVATUS_MEDIA_ROOT'] = 'media_dir'
    servatus.init_app(app)

    return app


class ServatusClassTests(unittest.TestCase):

    def test_set_default_servatus_storage_class(self):

        app = factory()

        self.assertEqual(
            app.config['SERVATUS_STORAGE_CLASS'],
            'flask_servatus.storages.FileSystemStorage')

    def test_user_defined_storage_class(self):

        app = Flask(__name__)
        app.config['SERVATUS_STORAGE_CLASS'] = 'foo.storage.MyStorage'
        app.config['SERVATUS_MEDIA_ROOT'] = 'media_dir'

        servatus.init_app(app)

        self.assertEqual(app.config['SERVATUS_STORAGE_CLASS'],
                         'foo.storage.MyStorage')

    def test_get_storage_class(self):

        app = factory()

        with app.app_context():
            self.assertEqual(servatus.get_storage_class(), FileSystemStorage)

    def test_media_root_required(self):

        app = Flask(__name__)
        app.config['SERVATUS_STORAGE_CLASS'] = 'foo.storage.MyStorage'

        with self.assertRaises(AttributeError):
            servatus.init_app(app)
