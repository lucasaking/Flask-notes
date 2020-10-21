from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", 
                           validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=3)])
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField("Last Name",
                             validators=[InputRequired(), Length(min=1, max=30)])
    email = StringField("Email", 
                        validators=[InputRequired(), Length(max=50)])


class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class NotesForm(FlaskForm):
    """Form for user adding notes. """

    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 20}, validators=[InputRequired()])


