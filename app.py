from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, NotesForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///user_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "donttell"

connect_db(app)
db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""
    
    if "user_id" not in session:
        return render_template("index.html")
    
    else:
        user = User.query.get_or_404(session["user_id"])
        return render_template("index.html", user=user)
    


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        pwd = form.password.data
        email = form.email.data

        user = User.register(username, pwd, first_name, last_name, email)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


# end-login


@app.route("/users/<username>")
def show_user_details(username):
    """Example hidden page for logged-in users only."""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        user = User.query.get_or_404(session["user_id"])
        return render_template("user_details.html", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    
    else:
        user = User.query.get_or_404(session["user_id"])
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id")
        flash(f"User has been deleted")
        return redirect("/")


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def show_notes_form(username):
    """ Display a form for user to add notes """

    form = NotesForm()
    

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    if form.validate_on_submit():
        user = User.query.get_or_404(session["user_id"])
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=user.username)
        db.session.add(note)
        db.session.commit()

        # session["user_id"] = user.id

        return redirect(f"/users/{user.username}")

    else:
        return render_template("notes_form.html", form=form)


# @app.route("/notes/<username>/notes/update")
# def update_notes_form():


