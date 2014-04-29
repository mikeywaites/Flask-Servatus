# -*- coding: utf-8 -*-
"""
    flask_servatus.fields
    ---------------

    Defines a `File` :class:`sqlalchemy.types.TypeDecorator` type that
    provides a simple interface to `flask_servatus` storages.

    .. seealso::
        :class:`flask_servatus.storages.Storage`

"""

from sqlalchemy import types

from flask_servatus import get_default_storage

from .files import ServatusFile


class File(types.TypeDecorator):
    """File :class:`sqlalchemy.types.Type` that supports the use of `storage
    backends`

    """

    impl = types.Unicode

    def __init__(self, storage=None, *args, **kwargs):
        self.storage = storage or get_default_storage()
        super(File, self).__init__(*args, **kwargs)

    def save(self, file):
        """save a file to the specified storage backend calling
        :meth:`storage.save`.

        :param file: a :class:`flask_servatus.files.ServatusFile` instance

        :raises: TypeError
        :returns: the file name of the saved file
        """
        if not isinstance(file, ServatusFile):
            raise TypeError('FileType requires a ServatusFile'
                            ' instance or subclass')

        return self.storage().save(file.name, file)

    def process_bind_param(self, file, dialect):

        return self.save(file)

    def process_result_value(self, value, dialect):
        """Return the fully qualified url for this `File`.

        """
        if value is not None:
            return self.storage().url(value)
        return value
