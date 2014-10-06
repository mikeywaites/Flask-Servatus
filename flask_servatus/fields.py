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


class FieldFile(ServatusFile):
    def __init__(self, storage, name):
        super(FieldFile, self).__init__(None, name=name)
        self.storage = storage

    def __hash__(self):
        return hash(self.name)

    # The standard File contains most of the necessary properties, but
    # FieldFiles can be instantiated without a name, so that needs to
    # be checked for here.

    def _require_file(self):
        if not self:
            raise ValueError("The no file associated.")

    def _get_file(self):
        self._require_file()
        if not hasattr(self, '_file') or self._file is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    def _set_file(self, file):
        self._file = file

    def _del_file(self):
        del self._file

    file = property(_get_file, _set_file, _del_file)

    def _get_path(self):
        self._require_file()
        return self.storage.path(self.name)
    path = property(_get_path)

    def _get_url(self):
        self._require_file()
        return self.storage.url(self.name)
    url = property(_get_url)

    def _get_size(self):
        self._require_file()
        return self.storage.size(self.name)
    size = property(_get_size)

    def open(self, mode='rb'):
        self._require_file()
        self.file.open(mode)
    # open() doesn't alter the file's contents, but it does reset the pointer
    open.alters_data = True

    def _get_closed(self):
        file = getattr(self, '_file', None)
        return file is None or file.closed
    closed = property(_get_closed)

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()


class File(types.TypeDecorator):
    """File :class:`sqlalchemy.types.Type` that supports the use of `storage
    backends`

    """

    impl = types.Unicode

    def __init__(self, storage=None, *args, **kwargs):
        self._storage = storage
        super(File, self).__init__(*args, **kwargs)

    @property
    def storage(self):
        return self._storage or get_default_storage()

    def save(self, file):
        """save a file to the specified storage backend calling
        :meth:`storage.save`.

        :param file: a :class:`flask_servatus.files.ServatusFile` instance

        :raises: TypeError
        :returns: the file name of the saved file
        """
        if not file:
            return

        servatus_file = ServatusFile.from_flask_filestorage(file)

        return self.storage.save(servatus_file.name, servatus_file)

    def process_bind_param(self, file, dialect):
        result = self.save(file)
        if result:
            return unicode(result)

    def process_result_value(self, value, dialect):
        """Return the fully qualified url for this `File`.

        """
        if value is not None:
            return FieldFile(self.storage, value)
            # return self.storage().url(value)
        return value
