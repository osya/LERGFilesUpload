# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask_uploads import configure_uploads, patch_request_class

from lerg_files_upload.extensions import (bcrypt, cache, csrf_protect, db, debug_toolbar, lergs, log, login_manager,
                                          migrate, webpack)
from lerg_files_upload.lerg.views import blueprint as lerg_blueprint
from lerg_files_upload.public.views import blueprint as public_blueprint
from lerg_files_upload.settings import ProdConfig
from lerg_files_upload.user.views import blueprint as user_blueprint


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    # TODO: Find the better way to serving static files in Flask in dev & prod
    app = Flask(__name__, static_url_path='/static', static_folder=os.path.join('static', 'dist'))
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    webpack.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    configure_uploads(app, lergs)
    patch_request_class(app, app.config['UPLOADS_MAX_FILESIZE'])
    log.init_app(app)
    log_file_name = os.path.join(app.config['APP_DIR'], 'static', app.config['LOG_FILE_NAME'])
    handler = RotatingFileHandler(log_file_name, maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(lerg_blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
