#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import StatementError
from sqlalchemy import Column, Integer

from .. import Servatus
from ..fields import File

servatus = Servatus()
db = SQLAlchemy()


def factory():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    servatus.init_app(app)
    db.init_app(app)

    return app


def get_model(db):

    class MyModel(db.Model):
        __tablename__ = 'my_model'
        id = Column(Integer, primary_key=True)
        image = Column(File(storage=servatus.get_storage_class()))

    return MyModel


class FieldTypeTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.app = factory()
        self.db = db
        ctx = self.app.test_request_context()
        ctx.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_file_type_requires_servatus_file_type(self):

        model = get_model(self.db)()
        model.image = 'foo'
        db.session.add(model)
        with self.assertRaises(StatementError):
            db.session.commit()

    def test_add_new_file_saves_file_using_storage(self):
        pass

    def test_model_with_existing_file_stored(self):
        pass

    def test_delete_existing_file_from_model(self):
        pass
