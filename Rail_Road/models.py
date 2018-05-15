from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from Rail_Road import db, login_manager


# Set up user_loader
@login_manager.user_loader
def load_user(id):
    return Passengers.query.get(int(id))


class Passengers(db.Model, UserMixin):
    __tablename__ = 'passengers'

    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.VARCHAR(30))
    lname = db.Column(db.VARCHAR(100))
    email = db.Column(db.VARCHAR(100))
    password = db.Column(db.VARCHAR(100))
    preferred_card_number = db.Column(db.VARCHAR(16))
    preferred_billing_address = db.Column(db.VARCHAR(100))

class Reservations(db.Model):
    __tablename__ = 'reservations'
    
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_date = db.Column(db.datetime)
    paying_passenger_id = db.Column(db.Integer,db.ForeignKey('passengers.passenger_id'))
    card_number = db.Column(db.VARCHAR(16))
    billing_address = db.Column(db.VARCHAR(100))
    
    def get_id(self):
        return self.passenger_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Passenger: {}, {}, {}>'.format(self.fname, self.lname, self.email)
