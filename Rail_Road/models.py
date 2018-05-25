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

    def get_id(self):
        return self.passenger_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Passenger: {}, {}, {}>'.format(self.fname, self.lname, self.email)

class Reservations(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_date = db.Column(db.DateTime)
    paying_passenger_id = db.Column(db.Integer,db.ForeignKey('passengers.passenger_id'))
    card_number = db.Column(db.VARCHAR(16))
    billing_address = db.Column(db.VARCHAR(100))

    def __repr__(self):
        return '<Passenger: {}, {}>'.format(self.reservation_id, self.reservation_date)


class Fare_types(db.Model):
    __tablename__ = 'fare_types'

    fare_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fare_name = db.Column(db.VARCHAR(20))
    rate = db.Column(db.Float)

    def get_id(self):
        return self.fare_id
    def get_rate(self):
        return self.rate
    def __repr__(self):
        return '<Fare_types: {}, {}>'.format(self.fare_name, self.rate)

class Station(db.Model):
    __tablename__ = 'stations'

    station_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_name = db.Column(db.VARCHAR(40))
    station_symbol = db.Column(db.CHAR(3))

    def get_id(self):
        return self.station_id
    def get_symbol(self):
        return self.station_symbol
    def __repr__(self):
        return '<Station: {}, {}, {}>'.format(self.station_id , self.station_name, self.station_symbol)

class Segments(db.Model):
    __tablename__ = 'segments'

    segment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seg_n_end = db.Column(db.Integer,db.ForeignKey('stations.station_id'))
    seg_s_end = db.Column(db.Integer,db.ForeignKey('stations.station_id'))
    seg_fare = db.Column(db.Float)

    def get_id(self):
        return self.segment_id
    def get_seg_n_end(self):
        return self.get_seg_n_end
    def get_seg_s_end(self):
        return self.get_seg_s_end
    def get_seg_fare(self):
        return self.seg_fare
    def __repr__(self):
        return '<Segments: {}, {}, {}, {}>'.format(self.segment_id , self.seg_n_end, self.seg_s_end, self.seg_fare)

class Trains(db.Model):
    __tablename__ = 'trains'

    train_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_start = db.Column(db.Integer,db.ForeignKey('stations.station_id'))
    train_end = db.Column(db.Integer,db.ForeignKey('stations.station_id'))
    train_direction = db.Column(db.Integer)
    train_days = db.Column(db.Integer)

    def get_id(self):
        return self.train_id

    def __repr__(self):
        return '<Trains: {}, {}, {}, {}, {}>'.format(self.train_id , self.train_start, self.train_end, self.train_direction, self.train_days)

class Seats_free(db.Model):
    __tablename__ = 'seats_free'

    train_id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer,db.ForeignKey('segments.segment_id'),primary_key=True)
    seat_free_date = db.Column(db.Date,primary_key=True)
    freeseat = db.Column(db.Integer)

    def get_train_id(self):
        return self.train_id

    def get_segment_id(self):
        return self.segment_id

    def __repr__(self):
        return '<Seats_free: {}, {}, {}, {}>'.format(self.train_id , self.segment_id, self.seat_free_date, self.freeseat)

class Stops_at(db.Model):
    __tablename__ = 'stops_at'

    train_id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'),primary_key=True)
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)

    def get_train_id(self):
        return self.train_id

    def get_station_id(self):
        return self.station_id
    def get_time_in(self):
        return self.time_in
    def get_time_out(self):
        return self.time_out
    def __repr__(self):
        return '<Stops_at: {}, {}, {}, {}>'.format(self.train_id , self.station_id, self.time_in, self.time_out)

class Trips(db.Model):
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    trip_date = db.Column(db.Date)
    trip_seg_start = db.Column(db.Integer,db.ForeignKey('segments.segment_id'))
    trip_seg_ends = db.Column(db.Integer,db.ForeignKey('segments.segment_id'))
    fare_type = db.Column(db.Integer, db.ForeignKey('fare_types.fare_id'))
    fare = db.Column(db.Float)
    trip_train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'))
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.reservation_id'))

    def get_id(self):
        return self.trip_id

    def __repr__(self):
        return '<Trips: {}, {}, {}, {}, {}, {}, {}, {}>'.format(self.trip_id , self.trip_date, self.trip_seg_start, self.trip_seg_ends,self.fare_type,self.fare,self.trip_train_id,self.reservation_id)
