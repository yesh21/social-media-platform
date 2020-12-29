from app import db
from flask_login import UserMixin
from datetime import datetime

followers = db.Table(
    'followers',
    db.Column('follower_id', db.String(500), db.ForeignKey('user.username')),
    db.Column('followed_id', db.String(500), db.ForeignKey('user.username'))
)

class User(db.Model, UserMixin):
	__tablename__ = "user"
	userid = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
	email = db.Column(db.String(70), unique=True, nullable=False)
	firstname = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(20), nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default= datetime.now())
	bio = db.Column(db.Text, nullable=False, default="add bio!")
	posts = db.relationship('Post', back_populates="userposts")
	followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == username),
                               secondaryjoin=(followers.c.followed_id == username),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
	def get_id(self):
           return (self.userid)
	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self
	def is_following(self, user):
		return self.followed.filter(
			followers.c.followed_id == user.username).count() > 0
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self
	def userfollowers(self, user):
		return self.followed.filter(
			followers.c.follower_id == user.username).count() > 0



class Post(db.Model):
	__tablename__ = "post"
	postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(500), nullable=False)
	user = db.Column(db.Integer, db.ForeignKey('user.userid'))
	date = db.Column(db.DateTime, nullable=False, default= datetime.now())
	message = db.Column(db.Text, nullable=False)
	userposts = db.relationship("User", back_populates="posts")

