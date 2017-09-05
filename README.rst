===============================
LERG Files Upload
===============================

.. image:: https://travis-ci.org/osya/LERGFilesUpload.svg?branch=master
    :target: https://travis-ci.org/osya/LERGFilesUpload/
    :alt: Build status

Flask & Jinja2-based webApp for LERG files (some special CSV files) uploading by admin and downloading these files by customers via API.

As though only admins will log in to this app the register link and register endpoint disabled. Admin login&password: admin:adminadmin

For testing used pytest, factory-boy, and WebTest


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export LERG_FILES_UPLOAD_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone http://valeriy@stash.denovolab.com/scm/ulu/alpha
    cd alpha\lerg_files_upload
    pip install -r requirements/dev.txt
    bower install
    python manage.py server


Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration:

::

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``LERG_FILES_UPLOAD_ENV`` environment variable is set to ``"prod"``.

Using
-----
To upload a file press "Choose File" button, choose file and press "Open" button. File will be uploaded and appears in Operation Log.

To download log press "Log Download" button

Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
