from app import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
	__tablename__ = "user"
	userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(500), nullable=False)
	firstname = db.Column(db.String(500), nullable=False)
	lastname = db.Column(db.String(500), nullable=False)
	username = db.Column(db.String(500), nullable=False)
	password = db.Column(db.String(500), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default= datetime.now())
	bio = db.Column(db.Text, nullable=False, default="add bio!")
	posts = db.relationship('Post', back_populates="userposts")
	def get_id(self):
           return (self.userid)


class Post(db.Model):
	__tablename__ = "post"
	postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(500), nullable=False)
	user = db.Column(db.Integer, db.ForeignKey('user.userid'))
	date = db.Column(db.DateTime, nullable=False, default= datetime.now())
	message = db.Column(db.Text, nullable=False)
	userposts = db.relationship("User", back_populates="posts")

