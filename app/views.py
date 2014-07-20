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
@login_required
def index():
    user = g.user
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

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))
                          
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
    
@app.before_request
def before_request():
    g.user = current_user