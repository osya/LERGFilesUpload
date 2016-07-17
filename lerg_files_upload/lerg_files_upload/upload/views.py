#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from forms import UploadForm

blueprint = Blueprint('upload', __name__, static_folder='../static')


@blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    form = UploadForm()

    if form.validate_on_submit():
        pass

    return render_template('upload/upload.html', form=form)
