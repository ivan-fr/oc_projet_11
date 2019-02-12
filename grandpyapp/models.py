from grandpyapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from grandpyapp import login


@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    photo = db.Column(db.String(255))
    street = db.Column(db.String(150))
    city = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    countries = db.Column(db.String(4))
    place_id = db.Column(db.String(150))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
