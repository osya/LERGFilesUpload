#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource


class LergAPI(Resource):
    def get(self):
        return {'todo_id': 1}
