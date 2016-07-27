#!/usr/bin/env python2.7
from bottle import route, run, template, response
from bottle import static_file

@route('/app/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/Users/klessinger/GitHub/misc_transcrypt/doc/kendo/src')

import json

def j(data):
    response.add_header('Content-Type', 'application/json')
    #return json.dumps(data['DDI']['columns'], indent=2, sort_keys=True)
    return json.dumps({'data': {'post': data}}, indent=2, sort_keys=True)

@route('/v1')
def index():
    from meta import meta
    return j(meta)

run(host='localhost', port=8080, reloader=True)

