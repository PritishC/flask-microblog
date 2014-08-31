# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 12:58:49 2014

@author: pritishc
"""

import os
import pytest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import User, Post

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
    
def test_follow_posts():
    u1 = User(nickname='john', email='john@example.com')
    u2 = User(nickname='susan', email='susan@example.com')
    u3 = User(nickname='mary', email='mary@example.com')
    u4 = User(nickname='david', email='david@example.com')
    for u in [u1, u2, u3, u4]:
        db.session.add(u)
    utcnow = datetime.utcnow()
    p1 = Post(body="post from john", author=u1, timestamp=utcnow+timedelta(seconds=1))
    p2 = Post(body="post from susan", author=u2, timestamp=utcnow+timedelta(seconds=2))
    p3 = Post(body="post from mary", author=u3, timestamp=utcnow+timedelta(seconds=3))
    p4 = Post(body="post from david", author=u4, timestamp=utcnow+timedelta(seconds=4))
    for p in [p1, p2, p3, p4]:
        db.session.add(p)
    db.session.commit()
    # setup followers.
    # To make the user see their own posts in the stream of followed posts,
    # we make them follow themselves.
    u1.follow(u1)
    u1.follow(u2)
    u1.follow(u4)
    u2.follow(u2)
    u2.follow(u3)
    u3.follow(u3)
    u3.follow(u4)
    u4.follow(u4)
    for u in [u1, u2, u3, u4]:
        db.session.add(u)
    db.session.commit()
    followed_posts = []
    for u in [u1, u2, u3, u4]:
        followed_posts.append(u.followed_posts().all())
    assert len(followed_posts[0]) == 3
    assert len(followed_posts[1]) == 2
    assert len(followed_posts[2]) == 2
    assert len(followed_posts[3]) == 1
    assert followed_posts[0] == [p4, p2, p1]
    assert followed_posts[1] == [p3, p2]
    assert followed_posts[2] == [p4, p3]
    assert followed_posts[3] == [p4]

def test_translation():
    from app.translate import microsoft_translate as mt
    assert mt(u'English', 'en', 'es') == u'Inglés'
    assert mt(u'Español', 'es', 'en') == u'Spanish'

def test_delete():
    u = User(nickname='john', email='whatevs@gmail.com')
    p = Post(body='test', author=u, timestamp=datetime.utcnow())
    db.session.add(u)
    db.session.add(p)
    db.session.commit()
    p = Post.query.get(1)
    db.session.remove()
    db.session = db.create_scoped_session()
    db.session.delete(p)
    db.session.commit()