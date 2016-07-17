# -*- coding: utf-8 -*-
"""User views."""
import lerg_files_upload.upload.views as upload_views
from flask import Blueprint, redirect, url_for
from flask_login import login_required

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    return redirect(url_for('upload.admin'))
