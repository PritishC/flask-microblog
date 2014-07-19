# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 19:23:42 2014

@author: pritishc
"""
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'} # fake user
    posts = [ #an array of fake posts
        {
            'author': {'nickname': 'John'},
            'body': 'OP is a faggot.'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'acualy is dolan'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)