# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 13:29:03 2014

@author: pritishc
"""

from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    
    def __repr__(self):
        return '<User {0!r}>'.format(self.nickname) # repr formatting.