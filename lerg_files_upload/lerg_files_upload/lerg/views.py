#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from forms import UploadForm
from lerg_files_upload.extensions import lergs


blueprint = Blueprint('lerg', __name__, static_folder='../static')


@blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    form = UploadForm()

    if form.validate_on_submit():
        if 'file_upload' in request.files and request.files['file_upload'].filename:
            lergs.save(request.files['file_upload'])

    return render_template('upload/upload.html', form=form)
