# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 13:29:03 2014

@author: pritishc
"""

from hashlib import md5
from app import db, app
import flask.ext.whooshalchemy as whooshalchemy
import re

ROLE_USER = 0
ROLE_ADMIN = 1

# The followers table is not written as a class.
# Instead, flask-sqlalchemy is used to generate the table.
# It is an association table meant to support our many-to-many relationship.
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id==id),
                               secondaryjoin=(followers.c.followed_id==id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return unicode(self.id)
        
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest()\
        + '?d=mm&s=' + str(size)
        
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
        
    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id==Post.user_id))\
                               .filter(followers.c.follower_id==self.id).order_by\
                               (Post.timestamp.desc())

    def sorted_posts(self):
        return self.posts.order_by(Post.timestamp_desc())
                               
    def __repr__(self): #pragma: no cover
        return '<User {0!r}>'.format(self.nickname) # repr formatting.
    
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname # in this case, no other user with this nickname exists, so no collisions.
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)
                
class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self): #pragma: no cover
        return '<Post {0!r}'.format(self.body)

whooshalchemy.whoosh_index(app, Post)