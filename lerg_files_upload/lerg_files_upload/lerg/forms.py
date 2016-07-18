#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import SubmitField
from wtformsparsleyjs import FileField


class UploadForm(Form):
    """
    Form for uploading LERG files
    """
    file_upload = FileField("Load Lerg file")
    submit = SubmitField('Upload')
