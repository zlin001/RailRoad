from flask import Flask, render_template, request, redirect, url_for, flash
from . import app, db
from flask_login import login_manager, current_user, login_user, logout_user, login_required
from Rail_Road.models import Passengers


# This is example for how to make a route for different page
@app.route('/')
# redirect to results page after search button is clicked at index page
@app.route('/index')
def index():
    return render_template("index.html")


# redirect to checkout page after reserve button is clicked at results page
@app.route('/results')
def results():
    return render_template("results.html")


# redirect to confirmation page after submit button is clicked at checkout page
@app.route('/checkout')
def checkout():
    return render_template("checkout.html")


# confirmation page returns the ticket info to user
@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")


# cancel trip
@app.route('/cancel')
def cancel():
    return render_template("cancel.html")


# ---------------------- REGISTERED PASSENGER ----------------------#
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if request.values.get('inputPd') == request.values.get('confirmPd'):
            check_email = Passengers.query.filter_by(email=request.values.get('inputEmail')).first()
            #flash("This is email is already used, please try another one")

            fname = request.values.get('first_name')
            lname = request.values.get('last_name')
            email = request.values.get('inputEmail')
            password = request.values.get('inputPd')
            cardnum = request.values.get('cardnum')
            addr1 = str(request.values.get('inputAddr'))
            addr2 = str(request.values.get('inputAddr2'))
            city = str(request.values.get('inputCity'))
            state = str(request.values.get('inputState'))
            zip = str(request.values.get('inputZip'))

            if check_email is None:
                billing_address = addr1 + (addr2 if addr2 == "" else (" " + addr2)) + ", " + city + ", " + state + ", " + zip

                passenger = Passengers(fname=fname, lname=lname, email=email, preferred_card_number=cardnum,
                                       preferred_billing_address=billing_address)

                passenger.set_password(password=password)
                db.session.add(passenger)
                db.session.commit()

                flash('Register successfully! You may login now.')

                return redirect(url_for('login'))
            else:
                flash("The email address is used, please try another one.")
        else:
            flash("Password does not match, please enter again.")
    return render_template("registration.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        passenger = Passengers.query.filter_by(email=request.values.get('email')).first()
        if passenger is None:
            flash("No matched record, please check your email or password again.")
        elif passenger is not None and passenger.check_password(request.values.get('password')):
            login_user(passenger)
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/profile')
@login_required
def profile():
    passenger = Passengers.query.filter_by(passenger_id=current_user.passenger_id).first()
    return render_template("profile.html", passenger=passenger)


# shows all tickets that the user has purchase
@app.route('/history')
def history():
    return render_template("history.html")


@app.route('/logout')
@login_required
def logout():
    flash("Logout successfully")
    logout_user()
    return redirect(url_for('index'))
