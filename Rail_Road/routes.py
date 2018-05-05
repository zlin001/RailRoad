from flask import Flask, render_template, request, redirect, url_for
from . import app

# This is exampel for how to make a route for different page
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# redirect to results page after search button is clicked at index page
@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/registration')
def registration():
    return render_template("registration.html")