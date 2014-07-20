# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 19:23:42 2014

@author: pritishc
"""
from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

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
                           
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash('Login requested for OpenID="' + login_form.openid.data + 
        '", remember_me=' + str(login_form.remember_me.data))
    return render_template('login.html',
                           title='Sign In',
                           form=login_form)