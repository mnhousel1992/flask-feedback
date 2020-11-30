from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost:5433/flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


# Login or register pages

@app.route("/")
def redirect_register():
    """Redirect to register page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Render form for registering a user and handle form submission"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Render form for login and handle form submission"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username

            return redirect(f"/users/{user.username}")

        else:
            form.username.errors("Bad username or password")

    else:
        return render_template("login.html", form=form)


# User page, delete user, logout

@app.route("/users/<username>")
def secret_page(username):
    """Render a secret page for logged in users only"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("user_page.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes a user from the database"""

    if 'username' not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/register")


@app.route("/logout")
def logout():
    """Logout user and redirect to homepage"""

    session.pop("username")
    return redirect("/login")


# Feedback pages

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Render new feedback form and handle submission"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.title.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Render update feedback form and handle submission"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():

        feedback.title = form.title.data
        feedback.content = form.title.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Render update feedback form and handle submission"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():

        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
