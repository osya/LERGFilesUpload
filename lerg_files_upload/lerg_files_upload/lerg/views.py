#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, app, jsonify, make_response
from forms import UploadForm
from lerg_files_upload.extensions import lergs, db
from lerg_files_upload.lerg.models import Lerg
import datetime as dt
from sqlalchemy import desc
import csv
import StringIO

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
    date = dt.datetime.strptime(date, "%Y-%m-%d")
    filename = Lerg.query.filter(Lerg.refresh_date <= date).order_by(desc(Lerg.refresh_date)).first().filename
    path = lergs.path(filename)
    with open(path, 'r') as f:
        body = f.read().decode('utf-8')
        response = make_response(body)
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@blueprint.route('/api/v1/getLergByCntState/<string:date>', methods=['GET', 'POST'])
def get_lerg_by_cnt_state(date):
    """
    Get the latest lerg closest to and before this date.
    Fields include should be NPANXX, Country, State
    """
    date = dt.datetime.strptime(date, "%Y-%m-%d")
    filename = Lerg.query.filter(Lerg.refresh_date <= date).order_by(desc(Lerg.refresh_date)).first().filename
    path = lergs.path(filename)

    with open(path, "rb") as source:
        rdr = csv.DictReader(source)
        keymap = dict((k.decode('utf-8'), k) for k in rdr.fieldnames)

        output = StringIO.StringIO()
        fieldnames = [u'Jurisdiction Name', u'State']
        wtr = csv.DictWriter(output, fieldnames=fieldnames)
        wtr.writeheader()

        for r in rdr:
            if r:
                wtr.writerow({u'Jurisdiction Name': r[keymap[u'﻿Jurisdiction Name']], 'State': r[keymap['State']]})

        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@blueprint.route('/api/v1/getLergByCntState2/<string:date>', methods=['GET', 'POST'])
def get_lerg_by_cnt_state2(date):
    """
    Get the latest lerg closest to and before this date.
    Fields include should be NPANXX, “US”, OCN-LATA
    """
    date = dt.datetime.strptime(date, "%Y-%m-%d")
    filename = Lerg.query.filter(Lerg.refresh_date <= date).order_by(desc(Lerg.refresh_date)).first().filename
    path = lergs.path(filename)

    with open(path, "rb") as source:
        rdr = csv.DictReader(source)
        keymap = dict((k.decode('utf-8'), k) for k in rdr.fieldnames)

        output = StringIO.StringIO()
        fieldnames = [u'Jurisdiction Name', u'State']
        wtr = csv.DictWriter(output, fieldnames=fieldnames)
        wtr.writeheader()

        for r in rdr:
            if r and 'US' == r[keymap[u'State']]:
                wtr.writerow({u'Jurisdiction Name': r[keymap[u'﻿Jurisdiction Name']], 'State': r[keymap['State']]})

        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response