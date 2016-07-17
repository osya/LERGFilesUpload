#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import SubmitField


class UploadForm(Form):
    """
    Form for uploading LERG files
    """
    submit = SubmitField('Submit')