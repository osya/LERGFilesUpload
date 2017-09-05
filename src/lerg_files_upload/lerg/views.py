#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import datetime as dt
import os.path as op
from io import StringIO

from flask import Blueprint, current_app, jsonify, make_response, render_template, request, send_file
from sqlalchemy import desc

from lerg_files_upload.extensions import db, lergs
from lerg_files_upload.lerg.forms import UploadForm
from lerg_files_upload.lerg.models import Lerg

blueprint = Blueprint('lerg', __name__, static_folder='../static')


@blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        if 'POST' == request.method and 'file_upload' in request.files and request.files['file_upload'].filename:
            filename = lergs.save(request.files['file_upload'])
            refresh_date = dt.datetime.utcnow()
            Lerg.create(filename=filename, refresh_date=refresh_date)
            current_app.logger.info('%s - Uploaded file %s' % (dt.datetime.utcnow(), filename))

    log_file_name = op.join(current_app.config['APP_DIR'], 'static', current_app.config['LOG_FILE_NAME'])
    with open(log_file_name, 'rU') as log_file:
        log_content = log_file.read()
    return render_template('upload/upload.html', form=form, log_content=log_content)


@blueprint.route('/api/v1/getLastRefresh', methods=['GET', 'POST'])
def get_last_refresh():
    """
    Return the last time the data is refreshed
    """
    last_refresh_date = db.session.query(db.func.max(Lerg.refresh_date)).scalar()
    return jsonify({'last_refresh_date': last_refresh_date})


@blueprint.route('/api/v1/getLerg/<string:date>', methods=['GET', 'POST'])
def get_lerg(date):
    """
    Get the latest lerg closest to and before this date
    """
    date = dt.datetime.strptime(date, '%Y-%m-%d')
    lerg = Lerg.query.filter(Lerg.refresh_date <= date).order_by(desc(Lerg.refresh_date)).first()
    if not lerg:
        return render_template('404.html'), 404
    filename = lerg.filename
    path = lergs.path(filename)
    with open(path, 'r') as f:
        body = f.read()
        response = make_response(body)
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@blueprint.route('/api/v1/getLergByCntState/<string:date>', methods=['GET', 'POST'])
def get_lerg_by_cnt_state(date):
    """
    Get the latest lerg closest to and before this date.
    Fields include should be NPANXX, Country, State
    """
    date = dt.datetime.strptime(date, '%Y-%m-%d')
    lerg = Lerg.query.filter(Lerg.refresh_date <= date).order_by(desc(Lerg.refresh_date)).first()
    if not lerg:
        return render_template('404.html'), 404
    filename = lerg.filename
    path = lergs.path(filename)

    with open(path, encoding='utf-8-sig') as source:
        rdr = csv.DictReader(source)
        keymap = dict((k, k) for k in rdr.fieldnames)

        output = StringIO()
        fieldnames = ['Jurisdiction Name', 'State']
        wtr = csv.DictWriter(output, fieldnames=fieldnames)
        wtr.writeheader()

        for r in rdr:
            if r:
                wtr.writerow({'Jurisdiction Name': r[keymap['Jurisdiction Name']], 'State': r[keymap['State']]})

        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@blueprint.route('/api/v1/getLergByCntState2/<string:date>', methods=['GET', 'POST'])
def get_lerg_by_cnt_state2(date):
    """
    Get the latest lerg closest to and before this date.
    Fields include should be NPANXX, “US”, OCN-LATA
    """
    date = dt.datetime.strptime(date, '%Y-%m-%d')
    lerg = Lerg.query.filter(Lerg.refresh_date <= date).order_by(desc(Lerg.refresh_date)).first()
    if not lerg:
        return render_template('404.html'), 404
    filename = lerg.filename
    path = lergs.path(filename)

    with open(path, encoding='utf-8-sig') as source:
        rdr = csv.DictReader(source)
        keymap = dict((k, k) for k in rdr.fieldnames)

        output = StringIO()
        fieldnames = ['Jurisdiction Name', 'State']
        wtr = csv.DictWriter(output, fieldnames=fieldnames)
        wtr.writeheader()

        for r in rdr:
            if r and 'US' == r[keymap['State']]:
                wtr.writerow({'Jurisdiction Name': r[keymap['Jurisdiction Name']], 'State': r[keymap['State']]})

        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@blueprint.route('/log')
def download_log():
    log_file_name = op.join(current_app.config['APP_DIR'], 'static', current_app.config['LOG_FILE_NAME'])
    return send_file(log_file_name, as_attachment=True)
