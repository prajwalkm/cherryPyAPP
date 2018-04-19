import os, os.path
import random
import string
import operator

import cherrypy

import json
from models import RedisDb
from controller import StringGenerator

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    webapp = StringGenerator()
    cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 8000})
    cherrypy.quickstart(webapp, '/', conf)