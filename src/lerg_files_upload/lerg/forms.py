#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtformsparsleyjs import FileField


class UploadForm(FlaskForm):
    """
    Form for uploading LERG files
    """
    file_upload = FileField('Load Lerg file')
    submit = SubmitField('Upload File')
