# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 12:58:49 2014

@author: pritishc
"""

import os
import pytest

from config import basedir
from app import app, db
from app.models import User

def setup_function(function):
    app.config['TESTING'] = True
    app.config['CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app_test = app.test_client()
    db.create_all()
    
def teardown_function(function):
    db.session.remove()
    db.drop_all()
    
def test_avatar():
    u = User(nickname = 'john', email = 'john@example.com')
    avatar = u.avatar(128)
    expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
    assert avatar[0:len(expected)] == expected
    
def test_make_unique_nickname():
    u = User(nickname = 'john', email = 'john@example.com')
    db.session.add(u)
    db.session.commit()
    nickname = User.make_unique_nickname('john')
    assert nickname != 'john'
    u = User(nickname = nickname, email = 'susan@example.com')
    db.session.add(u)
    db.session.commit()
    nickname2 = User.make_unique_nickname('john')
    assert nickname2 != 'john'
    assert nickname2 != nickname
    
def test_follow():
    u1 = User(nickname='john', email='john@lol.com')
    u2 = User(nickname='susan', email='susan@example.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    assert u1.unfollow(u2) == None # follow/unfollow either return the object or return None.
    u = u1.follow(u2)
    db.session.add(u)
    db.session.commit()
    assert u1.follow(u2) == None
    assert u1.is_following(u2)
    assert u1.followed.count() == 1
    assert u1.followed.first().nickname == 'susan'
    assert u2.followers.count() == 1
    assert u2.followers.first().nickname == 'john'
    u = u1.unfollow(u2)
    assert u != None
    db.session.add(u)
    db.session.commit()
    assert u1.is_following(u2) == False
    assert u1.followed.count() == 0
    assert u2.followers.count() == 0