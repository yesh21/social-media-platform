from app import db

def defaultIcon():
	return ""

class User(db.Model):
	__tablename__ = "user"
	userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(500), nullable=False)
	username = db.Column(db.String(500), nullable=False)
	password = db.Column(db.String(500), nullable=False)
	photo = db.Column(db.String(500), nullable=False, default=defaultIcon)
	posts = db.relationship('Post', back_populates="userposts")

class Post(db.Model):
	__tablename__ = "post"
	postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(500), nullable=False)
	user = db.Column(db.Integer, db.ForeignKey('user.userid'))
	message = db.Column(db.String(500), nullable=False)
	userposts = db.relationship("User", back_populates="posts")