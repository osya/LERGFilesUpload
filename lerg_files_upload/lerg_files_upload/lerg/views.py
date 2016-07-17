#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, app, jsonify
from forms import UploadForm
from lerg_files_upload.extensions import lergs, db
from lerg_files_upload.lerg.models import Lerg
import datetime as dt

blueprint = Blueprint('lerg', __name__, static_folder='../static')


@blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        if 'POST' == request.method and 'file_upload' in request.files and request.files['file_upload'].filename:
            filename = lergs.save(request.files['file_upload'])
            refresh_date = dt.datetime.utcnow()
            Lerg.create(filename=filename, refresh_date=refresh_date)

    return render_template('upload/upload.html', form=form)


@blueprint.route('/api/v1/getLastRefresh', methods=['GET', 'POST'])
def get_last_refresh():
    last_refresh_date = db.session.query(db.func.max(Lerg.refresh_date)).scalar()
    return jsonify({'last_refresh_date': last_refresh_date})
