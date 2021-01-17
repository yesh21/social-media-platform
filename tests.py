import os
import unittest

from flask import Flask

from app import app
from app import db, models

def add(x,y):
    return x + y

class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Post Data:

    # Test adding data to database
    def test_add_post_data(self):
        post = models.Post(title="testqwer", user="1", message="hello")
        db.session.add(post)
        db.session.commit()

        exists = models.Post.query.filter_by(title='testqwer').first()
        assert (exists is not None)

    # Test removing data from database
    def test_remove_post_data(self):
        models.Post.query.filter_by(title = "testqwer").delete()
        db.session.commit()

        exists = models.Post.query.filter_by(title='testqwer').first()
        assert (exists is None)

    # User Data:

    # Test adding data to database
    def test_add_user_data(self):
        user =models.User(username="test", email="test@example.com", password="test",lastname="test",firstname = "test")
        db.session.add(user)
        db.session.commit()

        exists = models.User.query.filter_by(email='test@example.com').first()   
        assert (exists is not None)

    # Test removing data from database
    def test_remove_user_data(self):
        models.User.query.filter_by(email='test@example.com').delete()
        db.session.commit()

        exists = models.User.query.filter_by(email='test@example.com').first()
        assert (exists is None)

if __name__ == '__main__':
    unittest.main()