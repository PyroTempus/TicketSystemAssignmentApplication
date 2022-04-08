from datetime import datetime
from ticketsystem import bcrypt
from ticketsystem import db, login_manager
from flask_login import UserMixin


# Code that tells the login manager where to find the users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Username database for storing admins
# UserMixin implements Flask methods for user login/logout operations
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    tickets = db.relationship('Ticket', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    # Setter that will hash the password when set automatically for us and decode once needed
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Checks to see if the attempted password equals the hashed password.
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


# Ticket database for storing and handling tickets
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.String(16), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Ticket %r>' % self.id