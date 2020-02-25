"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_form():

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():

    new_email = request.form.get("new_email")
    password = request.form.get("new_password")
    new_user = User(email=new_email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return render_template("homepage.html")

@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_check():
    your_email = request.form.get("your_email")
    your_password = request.form.get("your_password")
    if User.query.filter(User.email == your_email, User.password == your_password).all():
        flash("You successfully logged in!")
        return render_template("homepage.html")
    else:
        return render_template("unsuccessful_login.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
