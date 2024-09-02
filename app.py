"""Blogly application."""

# homepage.html, 404.html,

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'YtvJ x=\x92?\x8b8\xd0q\xfcFul\x11n\xe9y\x16\x8aa'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
debug = DebugToolbarExtension(app)
app.debug = True

with app.app_context():
    connect_db(app)
    db.create_all()

# Default routes

@app.route('/')
def home():
    """Home page"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND Page"""
    return render_template('404.html'), 404

 
# USER routes:


@app.route('/users')
def users_list():
    """Show all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users = users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Form to create a new User"""
    return render_template('users/form.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user = user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited")

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")


# ------------------------------------------------------------------------ #
# Blogly app pt 2                                                          #
# ------------------------------------------------------------------------ #


