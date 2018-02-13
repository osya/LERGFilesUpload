# LERG Files Upload

## Introduction

[![Build Status](https://travis-ci.org/osya/LERGFilesUpload.svg?branch=master)](https://travis-ci.org/osya/LERGFilesUpload/) [![Coverage Status](https://coveralls.io/repos/github/osya/LERGFilesUpload/badge.svg?branch=master)](https://coveralls.io/github/osya/LERGFilesUpload?branch=master)

It is a Flask & Jinja2-based webApp for LERG files (some special CSV files) uploading by admin and downloading these files by customers via API.

As though only admins will log in to this app the register link and register endpoint disabled. Admin login&password: admin:adminadmin

Used technologies:

- Testing: pytest, factory-boy, and WebTest
- Assets management: NPM & Webpack
- Travis CI

## Installation

First, set your app's secret key as an environment variable. For example, example add the following to `.bashrc` or `.bash_profile`.

```bash
    export LERG_FILES_UPLOAD_SECRET='something-really-secret'
```

In your production environment, make sure the `LERG_FILES_UPLOAD_ENV` environment variable is set to `"prod"`.

Then run the following commands to bootstrap your environment.

```shell
    git clone https://github.com/osya/LERGFilesUpload
    cd LERGFilesUpload
    pip install -r requirements/dev.txt
    npm install
    node node_modules/webpack/bin/webpack.js
```

Migrate your database and run `python manage.py server`

### Migrations

Whenever a database migration needs to be made (for example, once you have installed your DBMS). Run the following commands:

```shell
    python manage.py db init
    python manage.py db migrate
```

This will generate a new migration script. Then run `python manage.py db upgrade` to apply the migration.

For a full migration command reference, run `python manage.py db --help`.

## Usage

To upload a file press "Choose File" button, choose file and press "Open" button. File will be uploaded and appears in Operation Log.

To download log press "Log Download" button

### Shell

To open the interactive shell, run `python manage.py shell`

By default, you will have access to `app`, `db`, and the `User` model.

## Tests

To run all tests, run

```shell
    python manage.py test
```
