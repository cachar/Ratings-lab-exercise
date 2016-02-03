"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/sign-in-form')
def sign_in_form():
    """Shows the user a form to put in info."""

    return render_template("sign_in.html")

@app.route('/sign-in', methods=["POST"])
def sign_in():
    """Have the user signed in."""
    
    email = request.form.get("email")
    print email
    password = request.form.get("password")
    print password

    user = User.query.filter(User.email == email).first()

    if user == None: 
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    
    print user, "TEST"

    return "Success!"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logged-in', methods=["POST"])
def logged_in():
    """Users with an account can login."""

    pass  

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
