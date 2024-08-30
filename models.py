"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

# Models

class User(db.Model):
    """instance of a user for the blog app"""

    __tablename__ = "users"

    # class methods go here

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)

    first_name = db.Column(db.String(20),nullable = False)
    
    last_name = db.Column(db.String(20), nullable = False,)
    
    image_url = db.Column(db.Text, 
                          nullable = False, 
                          default = DEFAULT_IMAGE_URL)
    

def connect_db(app):
    """Connect this database to provided Flask app"""
    db.app = app
    db.init_app(app)