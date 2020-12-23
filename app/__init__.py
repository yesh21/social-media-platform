from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
#app.config.from_object('config')
import os
WTF_CSRF_ENABLED = True
SECRET_KEY = 'bigtoe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#app.config.from_object('config')

db = SQLAlchemy(app)

#migrate = Migrate(app, db)
db.create_all()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
from app import models