Quickstart
==========

.. include:: header.rst


**1** :ref:`Install Flask-Servatus <installation>` via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sourcecode:: shell

    $ pip install Flask-Servatus


**2** :ref:`Initialise <initialise>` and :ref:`configure <configuration>` the ``Servatus`` application object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sourcecode:: python

    from flask import Flask
    from flask.ext.servatus import Servatus

    app = Flask(__name__)
    servatus = Servatus(app)

    #.init_app() interface is also availble..

    def factory(arg, arg2):

        app = Flask(__name__)
        servatus = Servatus()
        servatus.init_app(app)

        return app



**3** Use your prefered :ref:`storages <storages>` object to save files.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sourcecode:: python

    from flask import Flask
    from flask.ext.servatus import Servatus
    from flask.ext.servatus.files import ContentFile
    from flask.ext.servatus.storages import get_default_storage

    app = Flask(__name__)
    servatus = Servatus(app)

    storage = get_default_storage()

    @app.route('/uploads', methods=['GET', 'POST'])
    def handle_upload():
        # handle uploaded file from user subitted form..

        storage.save('foo.txt', request.files['file'])

