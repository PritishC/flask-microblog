#!/home/pritishc/Envs/ircflask/bin/python

__author__ = 'pritishc'

from werkzeug.contrib.profiler import ProfilerMiddleware
from app import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
app.run(debug = True)