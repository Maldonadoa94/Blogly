"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect this database to provided Flask app"""
    db.app = app
    db.init_app(app)

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
    
    posts = db.relationship("Post", backref = "user", cascade = "all, delete-orphan")

    @property
    def full_name(self):
        """return's user's full name"""
        return f"{self.first_name} {self.last_name}"
    

# ------------------------------------------------------------------------ #
# Blogly app pt 2                                                          #
# ------------------------------------------------------------------------ #


class Post(db.Model):
    """instance of a blog post created by users"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.Text, nullable = False)

    content = db.Column(db.Text, nullable = False)

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.datetime.now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    @property
    def friendly_date(self):
        """format date"""
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    