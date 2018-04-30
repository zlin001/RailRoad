from flask import Flask, render_template, request
from . import app

# This is exampel for how to make a route for different page
@app.route("/")
def index():
    return render_template("index.html")
