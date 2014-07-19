# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 20:35:35 2014

@author: pritishc
"""

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)
    
    