# -*- coding: utf-8 -*-
"""Application configuration."""
import os

from decouple import config


class Config(object):
    """Base configuration."""

    SECRET_KEY = config('SECRET_KEY')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    LOG_FILE_NAME = 'lerg.log'
    UPLOADED_FILES_DEST = config('UPLOADED_FILES_DEST', default=os.path.join(APP_DIR, 'static', 'uploaded_lergs'))
    UPLOADS_MAX_FILESIZE = 16 * 1024 * 1024  # max request at 16 megabytes
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = config('DEBUG_TB_ENABLED', default=False, cast=bool)  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = config('DEBUG_TB_INTERCEPT_REDIRECTS', default=False, cast=bool)
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEBPACK_MANIFEST_PATH = os.path.join(APP_DIR, 'static', 'dist', 'manifest.json')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = config('DEBUG_TB_ENABLED', default=False, cast=bool)
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'  # TODO: Change me


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = config('DEBUG_TB_ENABLED', default=True, cast=bool)
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
