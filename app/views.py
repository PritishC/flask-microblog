# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 19:23:42 2014

@author: pritishc
"""
from flask import render_template, flash, redirect, session, url_for, request,g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

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
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['remember_me'] = login_form.remember_me.data
        return oid.try_login(login_form.openid.data, ask_for = ['nickname',
                                                                'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=login_form,
                           providers=app.config['OPENID_PROVIDERS'])
                          
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))