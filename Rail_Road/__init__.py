# getting flask
from flask import Flask
# set the app to improv_app
app = Flask('Rail_Road')
# getting routes
from Rail_Road import routes
from flask_bootstrap import Bootstrap

Bootstrap(app)
