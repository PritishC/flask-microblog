# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 20:18:43 2014

@author: pritishc
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True #Cross-site request forgery prevention
SECRET_KEY = 'dbz3:Treemight'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
    
# mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'fakeusepritish@gmail.com'
MAIL_PASSWORD = 'ifreakingknewit'

# admin list
ADMINS = ['fakeusepritish@gmail.com', 'chakrabortypritish@gmail.com']

# pagination
POSTS_PER_PAGE = 3

# text search
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# supported langs for Babel
LANGUAGES = {'en': 'English', 'es': 'Español',}

# Microsoft Translator service details
MS_TRANSLATOR_CLIENT_ID = "flask-microblog"
MS_TRANSLATOR_CLIENT_SECRET = "z3WPPknJxbNIj+hPASkiYqluDQNkBOijARxDFsVtTYY="