from flask import Flask, render_template, request, redirect, url_for, flash
from . import app, db
from flask_login import login_manager, current_user, login_user, logout_user, login_required
from Rail_Road.models import Passengers, Reservations,Fare_types, Station, Segments, Trains, Seats_free, Stops_at, Trips
from datetime import datetime, date, time

# This is example for how to make a route for different page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        passenger = Passengers.query.filter_by(email=request.values.get('email')).first()
        if passenger is None:
            flash("No matched record, please check your email.")
        elif passenger is not None and passenger.check_password(request.values.get('password')):
            login_user(passenger)
            return redirect(url_for('index'))
        else:
            flash("Password does not match, please check again")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")



# redirect to results page after search button is clicked at index page
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    stations = Station.query.all()

    if request.method == 'POST':
        #session['session'] = session
        #session['date'] = date
        #session['type'] = type
        return redirect(url_for('results'))

    return render_template("index.html", stations=stations)


# redirect to checkout page after reserve button is clicked at results page
@app.route('/results',methods=['GET','POST'])
@login_required
def results():
    result = []
    session_input = request.args.get("session")
    date_input = request.args.get("datepicker")
    type_input = request.args.get("ticket_type")
    start_station_input = request.args.get("start_station")
    end_station_input = request.args.get("end_station")
    pet_input = request.args.get("pet")
    start_station = Station.query.filter_by(station_name=start_station_input).first()
    end_station = Station.query.filter_by(station_name=end_station_input).first()
    sum = 0
    if start_station == None or end_station == None:
        return render_template("results.html",start_station=start_station_input,end_station=end_station_input,date=date_input,result=result)
    if start_station.get_id() == end_station.get_id():
        return render_template("results.html",start_station=start_station.get_symbol(),end_station=end_station.get_symbol(),date=date_input,result=result)
    if start_station.get_id() > end_station.get_id():
        train_direction = 1
        start_segment = Segments.query.filter_by(seg_s_end = start_station.get_id()).first()
        end_segment = Segments.query.filter_by(seg_n_end = end_station.get_id()).first()
        difference_id = start_station.get_id() - end_station.get_id()
        for i in range(difference_id):
            sum += Segments.query.filter_by(seg_n_end = i + end_station.get_id()).first().get_seg_fare()
    else:
        train_direction = 0
        start_segment = Segments.query.filter_by(seg_n_end = start_station.get_id()).first()
        end_segment = Segments.query.filter_by(seg_s_end = end_station.get_id()).first()
        difference_id = end_station.get_id() - start_station.get_id()
        for i in range(difference_id):
            sum += Segments.query.filter_by(seg_n_end = i + start_station.get_id()).first().get_seg_fare()
    rate = 0
    if pet_input == "pet":
        type = Fare_types.query.filter_by(fare_name = type_input).first()
        rate = type.get_rate() + Fare_types.query.filter_by(fare_name = "pets").first().get_rate()
    else:
        type = Fare_types.query.filter_by(fare_name = type_input).first()
        rate = type.get_rate()
    # print(rate)
    #print(sum)
    current_datetime = datetime.now()
    # print(start_segment.get_id())
    # print(end_segment.get_id())
    if session_input == "morning":
        start_time = datetime.strptime(date_input + " 06:00:00", "%m/%d/%Y %H:%M:%S")
        end_time = datetime.strptime(date_input + " 12:00:00", "%m/%d/%Y %H:%M:%S")
    elif session_input == "afternoon":
        start_time = datetime.strptime(date_input + " 12:00:01", "%m/%d/%Y %H:%M:%S")
        end_time = datetime.strptime(date_input + " 17:00:00", "%m/%d/%Y %H:%M:%S")
    else:
        start_time = datetime.strptime(date_input + " 17:00:01", "%m/%d/%Y %H:%M:%S")
        end_time = datetime.strptime(date_input + " 05:59:59", "%m/%d/%Y %H:%M:%S")
    if start_time < current_datetime:
        return render_template("results.html",start_station=start_station.get_symbol(),end_station=end_station.get_symbol(),date=date_input,result=result)
    sum_days_current = current_datetime.year * 365 + current_datetime.month * 30 + current_datetime.day
    target_days = start_time.date().year * 365 + start_time.date().month * 30 + start_time.date().day
    ratio_date = sum_days_current/target_days
    #print(ratio_date)
    if ratio_date > 0.6:
        rate = rate + (0.1 * ratio_date)
    total = rate * sum
    total = round(total,2)
    start_stops_at = Stops_at.query.filter(Stops_at.time_in >= start_time.time(), Stops_at.time_in <= end_time.time(), Stops_at.station_id == start_station.get_id()).all()
    meet_date_list = {}
    for data in start_stops_at:
        meet_date_train = Seats_free.query.filter_by(train_id = data.get_train_id(),seat_free_date = start_time.date()).all()
        if len(meet_date_train) != 0:
            meet_date_list[data.get_train_id()] = Seats_free.query.filter_by(train_id = data.get_train_id(),segment_id=start_segment.get_id(),seat_free_date = start_time.date()).all()
    #print(meet_date_list)
    direction_train_list = []
    for key in meet_date_list:
        if Trains.query.filter_by(train_id=key,train_direction=train_direction).first() != None:
            direction_train_list.append(key)
        #print(direction_train_list)
    information = {}
    train_list_with_seat = []
    seat_number = []
    for i in range(len(direction_train_list)):
        smaller_seat = 448
        if train_direction == 0:
            for x in range(difference_id):
                begin = Segments.query.filter_by(seg_n_end = x + start_station.get_id()).first().get_id()
                freeseat_no = Seats_free.query.filter_by(train_id = direction_train_list[i], segment_id = begin,seat_free_date = start_time.date()).first().get_freeseat()
                if freeseat_no <= smaller_seat:
                    smaller_seat = freeseat_no
            if smaller_seat != 0:
                seat_number.append(smaller_seat)
                train_list_with_seat.append(direction_train_list[i])
        else:
            for x in range(difference_id):
                begin = Segments.query.filter_by(seg_n_end = x + end_station.get_id()).first().get_id()
                freeseat_no = Seats_free.query.filter_by(train_id = direction_train_list[i], segment_id = begin,seat_free_date = start_time.date()).first().get_freeseat()
                if freeseat_no <= smaller_seat:
                    smaller_seat = freeseat_no
            if smaller_seat != 0:
                seat_number.append(smaller_seat)
                train_list_with_seat.append(direction_train_list[i])
    for i in range(len(train_list_with_seat)):
        information["train_no"] = direction_train_list[i]
        if train_direction == 0:
            information["depature time"] = Stops_at.query.filter_by(train_id = direction_train_list[i],station_id=start_station.get_id()).first().get_time_in().strftime('%H:%M:%S')
            information["arrival time"] = Stops_at.query.filter_by(train_id = direction_train_list[i],station_id=end_station.get_id()).first().get_time_out().strftime('%H:%M:%S')
        else:
            information["depature time"] = Stops_at.query.filter_by(train_id = direction_train_list[i],station_id=end_station.get_id()).first().get_time_in().strftime('%H:%M:%S')
            information["arrival time"] = Stops_at.query.filter_by(train_id = direction_train_list[i],station_id=start_station.get_id()).first().get_time_out().strftime('%H:%M:%S')
        information["price"] = total
        information["seat_number"] = seat_number[i]
        information["fare_type"] = type_input
        information["trip_seg_start"] = start_segment.get_id()
        information["trip_seg_ends"] = end_segment.get_id()
        result.append(information.copy())
    if request.method == "GET":
        return render_template("results.html",start_station=start_station.get_symbol(),end_station=end_station.get_symbol(),date=date_input,result=result)
    elif request.method == "POST":
        passenger = Passengers.query.filter_by(passenger_id=current_user.passenger_id).first()
        for information in result:
          if request.form.get(str(information["train_no"])) != None:
                selected_information = information
        #print(selected_information)
        trip = Trips(trip_date = start_time.date(), trip_seg_start=selected_information["trip_seg_start"],trip_seg_ends = selected_information["trip_seg_ends"],fare_type = type.get_id(), fare = total, trip_train_id = selected_information["train_no"])
        db.session.add(trip)
        db.session.commit()
        if train_direction == 0:
            for i in range(difference_id):
                begin = Segments.query.filter_by(seg_n_end = i + start_station.get_id()).first().get_id()
                update_seat = Seats_free.query.filter_by(train_id = selected_information["train_no"],seat_free_date = start_time.date(),segment_id = begin).first()
                update_seat.freeseat = update_seat.get_freeseat() - 1
                db.session.commit()
        else:
            for i in range(difference_id):
                begin = Segments.query.filter_by(seg_n_end = i + end_station.get_id()).first().get_id()
                update_seat = Seats_free.query.filter_by(train_id = selected_information["train_no"],seat_free_date = start_time.date(),segment_id = begin).first()
                update_seat.freeseat = update_seat.get_freeseat() - 1
                db.session.commit()
        return render_template("checkout.html",passenger=passenger)



# redirect to confirmation page after submit button is clicked at checkout page
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    passenger = Passengers.query.filter_by(passenger_id=current_user.passenger_id).first()
    now = datetime.now()
    if request.method == 'POST':
        fname = request.values.get('first_name')
        lname = request.values.get('last_name')
        cardnum = request.values.get('cardnum')
        addr1 = str(request.values.get('inputAddr'))
        addr2 = str(request.values.get('inputAddr2'))
        city = str(request.values.get('inputCity'))
        state = str(request.values.get('inputState'))
        zip = str(request.values.get('inputZip'))
        user = current_user.passenger_id
        billing_address = addr1 + (addr2 if addr2 == "" else (" " + addr2)) + ", " + city + ", " + \
                          state + ", " + zip
        date = now.strftime("%Y-%m-%d %H:%M")
        reservation = Reservations(reservation_date=date, paying_passenger_id=user, card_number=cardnum,
                                   billing_address=billing_address)
        db.session.add(reservation)
        db.session.commit()

        flash('Reservation Made!')
        return render_template("confirmation.html", reservation_id=reservation.reservation_id)

    return render_template("checkout.html", passenger=passenger)


# confirmation page returns the ticket info to user
@app.route('/confirmation/<reservation_id>')
@login_required
def confirmation(reservation_id):
    #reservation = Reservations.query.filter_by(reservation_id=reservation_id).first
    return render_template("confirmation.html", reservation_id=reservation_id)


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
            # flash("This is email is already used, please try another one")

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
                billing_address = addr1 + (addr2 if addr2 == "" else (" " + addr2)) + ", " + city + ", " + \
                                  state + ", " + zip

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
    return redirect(url_for('login'))
