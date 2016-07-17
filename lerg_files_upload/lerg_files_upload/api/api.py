#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.views import MethodView
from lerg_files_upload.extensions import app


class LergAPI(MethodView):

    '''
    getLastRefresh()
    Return the last time the data is refreshed
    getLerg(Date)
    Get the latest lerg closest to and before this date.
    getLergByCntState(Date)
    Get the latest lerg closest to and before this date.
    Fields include should be NPANXX, Country, State
    getLergByCntState(Date)
    '''

    # def get(self):
    #     return session.get('counter', 0)
    #
    # def post(self):
    #     session['counter'] = session.get('counter', 0) + 1
    #     return 'OK'

app.add_url_rule('/api', view_func=LergAPI.as_view('api'))