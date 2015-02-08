#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import tempfile

from os.path import dirname, join, exists

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import StatementError
from sqlalchemy import Column, Integer

from flask_servatus import Servatus
from flask_servatus.fields import File
from flask_servatus.files import ContentFile
import shutil


servatus = Servatus()

MEDIA_DIR = join(dirname(__file__), 'test_media')


def factory(db):

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SERVATUS_MEDIA_ROOT'] = MEDIA_DIR
    servatus.init_app(app)
    db.init_app(app)

    return app


def get_model(db):

    class MyModel(db.Model):
        __tablename__ = 'my_model'
        id = Column(Integer, primary_key=True)
        image = Column(File(storage=servatus.get_default_storage()))

    return MyModel


class FieldTypeTests(unittest.TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.temp_dir = tempfile.mkdtemp()
        self.app = factory(self.db)
        ctx = self.app.test_request_context()
        ctx.push()
        self.Model = get_model(self.db)
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()
        if exists(MEDIA_DIR):
            shutil.rmtree(MEDIA_DIR)

    def test_file_type_requires_servatus_file_type(self):
        model = self.Model()
        model.image = 'foo'
        self.db.session.add(model)
        with self.assertRaises(StatementError):
            self.db.session.commit()

    def test_add_new_file_saves_file_using_storage(self):
        model = self.Model()
        model.image = ContentFile('foo', name='foo.txt')
        self.db.session.add(model)

        self.db.session.commit()

        self.assertTrue(exists(model.image.path))

    def test_url_set(self):
        model = self.Model()
        model.image = ContentFile('foo', name='foo.txt')
        self.db.session.add(model)

        self.db.session.commit()

        self.assertEquals(model.image.url, '/media/foo.txt')

    def test_size_set(self):
        model = self.Model()
        model.image = ContentFile('foo', name='foo.txt')
        self.db.session.add(model)

        self.db.session.commit()

        self.assertEquals(model.image.size, 3)

    def test_model_with_existing_file_stored(self):
        model = self.Model()
        model.image = ContentFile('foo', name='foo.txt')
        self.db.session.add(model)

        self.db.session.commit()

        self.db.session.add(model)

        model.image = ContentFile('foo2', name='foo2.txt')

        self.db.session.commit()

        self.assertTrue(model.image.path.endswith('foo2.txt'))

    def test_delete_existing_file_from_model(self):
        model = self.Model()
        model.image = ContentFile('foo', name='foo.txt')
        self.db.session.add(model)

        self.db.session.commit()

        self.db.session.add(model)

        model.image = None

        self.db.session.commit()

        self.assertIsNone(model.image)

        # TODO: should delete the existing file but it does not atm
