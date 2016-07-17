#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lerg_files_upload.database import Model, SurrogatePK, Column
from lerg_files_upload.extensions import db


class Lerg(SurrogatePK, Model):
    filename = Column(db.String())
    refresh_date = Column(db.DateTime())
