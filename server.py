import json
from datetime import datetime

from flask import Flask,render_template,request,redirect,flash,url_for


MAX_PLACES = 12

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'


competitions = loadCompetitions()
clubs = loadClubs()
current_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

cart = {
    competition['name']: {club['name']: 0 for club in clubs}
    for competition in competitions
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
@app.errorhandler(400)
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)

    except IndexError:
        flash("Sorry, this email wasn't found.")
        return redirect(url_for('index')), 400


@app.route('/book/<competition>/<club>')
@app.errorhandler(400)
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except(IndexError):
        flash("Sorry, something went wrong. Please try again")
        return render_template('welcome.html', club=club, competitions=competitions), 400


@app.route('/purchasePlaces', methods=['POST'])
@app.errorhandler(400)
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    clubPoints = int(club['points'])
    placesRequired = int(request.form['places'])
    current_cart = cart[competition['name']][club['name']]

    if competition['date'] < current_date:
        flash("Sorry, this competition is over")
        return render_template('welcome.html', club=club, competitions=competitions), 400  

    elif placesRequired > int(competition['numberOfPlaces']) :
        flash("Sorry, the competition doesn\'t have enough places")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    elif placesRequired > MAX_PLACES :
        flash(f"Sorry, you can't book more than {MAX_PLACES} places")
        return render_template('booking.html', club=club, competition=competition), 400

    elif placesRequired > clubPoints:
        flash("Sorry, your club doesn't have enough points")
        return render_template('booking.html', club=club, competition=competition), 400

    elif placesRequired + current_cart > MAX_PLACES:
        flash(f"""Sorry, you have already booked {current_cart} places for this competition 
        and you can't book more than {MAX_PLACES}""")
        return render_template('booking.html', club=club, competition=competition), 400

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    cart[competition["name"]][club["name"]] += placesRequired

    flash(f"Great you have booked {placesRequired} places for {competition['name']}")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/showBoard', methods=['GET'])
def showBoard():
    return render_template('board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))