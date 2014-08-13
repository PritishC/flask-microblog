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
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 25
MAIL_USERNAME = 'fakeusepritish@gmail.com'
MAIL_PASSWORD = 'ifreakingknewit'

# admin list
ADMINS = ['pritish@guerrillamail.com', 'chakrabortypritish@gmail.com']

# pagination
POSTS_PER_PAGE = 3