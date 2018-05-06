# getting flask
from flask import Flask
# set the app to improv_app
app = Flask('Rail_Road')
# getting routes
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from flask_login import LoginManager

Bootstrap(app)

server = SSHTunnelForwarder(
    ('134.74.126.104', 22),  # 104
    ssh_username='caiz4042',
    ssh_password='23424042',
    remote_bind_address=('134.74.146.21', 3306))
server.start()
engine = create_engine('mysql+pymysql://S18336Pteam7:rowayton@127.0.0.1:%s/S18336Pteam7' % server.local_bind_port)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://S18336Pteam7:rowayton@127.0.0.1:%s/S18336Pteam7' % server.local_bind_port
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
db = SQLAlchemy(app)
app.config.update(dict(SECRET_KEY="*&%$xs13#^"))

from Rail_Road import routes, models
from Rail_Road.models import Passengers

# test db
# passenger = Passengers(fname="aaa", lname="bbb", email="aaa@example.com", preferred_card_number="123456789",
#                        preferred_billing_address="123 45th st, New York, NY, 12345")
# passenger.set_password("1234")
# db.session.add(passenger)
# db.session.commit()