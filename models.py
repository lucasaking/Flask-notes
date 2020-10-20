from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(30),
                         nullable=False)

    last_name = db.Column(db.String(30),
                         nullable=False)

    email = db.Column(db.String(50),
                         nullable=False)

    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)

    password = db.Column(db.Text,
                         nullable=False)

    notes = db.relationship('Note')


    # start_register
    @classmethod
    def register(cls, username, pwd, first_name, last_name, email):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed, first_name=first_name, last_name=last_name, email=email)

    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate

class Note(db.Model):

    __tablename__ = "notes"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(50),
                      nullable=True)

    content = db.Column(db.Text,
                        nullable=True)

    owner = db.Column(db.String,
                      db.ForeignKey("users.username"))
    
    user = db.relationship('User')
