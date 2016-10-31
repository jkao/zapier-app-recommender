#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import bottle

from bottle import *
from os import environ as env
from sys import argv

import search
from data import cleaner

dc = cleaner.DataCleaner()
zs = search.ZapSearch(esUrl=argv[2], cleaner=dc)

# serves the homepage
@get('/')
def index():
    return template('zapapp/views/main.tpl')

# essentially a proxy to ES
@get('/search')
def search():
    response.content_type = 'application/json'
    return json.dumps(zs.search(request.query.query))

# static files
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='zapapp/static')

if __name__ == "__main__":
    bottle.debug(True) # TODO(jeffk)
    bottle.run(host='0.0.0.0', port=argv[1])
