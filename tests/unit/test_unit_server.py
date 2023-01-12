import pytest
from flask import url_for


##########################  login  ###############################


def test_login_success(client):
    response = client.get('/')
    assert 'Welcome to the GUDLFT Registration' in response.data.decode()

def test_login_not_found(client):
    response = client.get('/welcome')
    assert response.status_code == 404


##########################  logout  ###############################


def test_logout_success(client):
    response = client.get('/logout')
    assert response.headers["location"] == '/'


##########################  showSummary  ###############################


def test_showSummary_success(client, clubs_data):
    club = clubs_data[0]

    response = client.post('/showSummary', data={'email': club['email']})

    assert response.status_code == 200

def test_showSummary_club_not_found(client, clubs_data):
    response = client.post('/showSummary', data={'email': 'invalid@example.com'})

    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, this email wasn't found."


##############################  book  ##################################


def test_book_success(client, clubs_data, competitions_data):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')

    assert response.status_code == 200
    assert str(club['name']) in response.data.decode()

def test_book_club_not_found(client, competitions_data):
    competition = competitions_data[0]
    response = client.get(f'/book/{competition["name"]}/ClubD')

    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, something went wrong. Please try again"

def test_book_competition_not_found(client, clubs_data):
    club = clubs_data[0]
    response = client.get(f'/book/Competition4/{club["name"]}')

    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, something went wrong. Please try again"


##########################  purchasePlaces  ###############################


def test_purchasePlaces_success(client, clubs_data, competitions_data):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 1,
    })

    assert response.status_code == 200

def test_purchasePlaces_competition_over(client, clubs_data, competition_over):
    club = clubs_data[0]
    competition = competition_over

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 1,
    })

    assert response.status_code == 400
    
def test_purchasePlaces_more_than_maxPlaces(client, clubs_data, competitions_data):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 14,
    })

    assert response.status_code == 400

def test_purchasePlaces_more_than_nbPlaces(client, clubs_data, competitions_data):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 100,
    })

    assert response.status_code == 400

def test_purchasePlaces_more_than_nbPlaces(client, clubs_data, competitions_data):
    club = clubs_data[2]
    competition = competitions_data[1]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 7,
    })

    assert response.status_code == 400


##########################  showSummary  ###############################


def test_showBoard_success(client, clubs_data):
    response = client.get('/showBoard')
    for club in clubs_data:
        assert str(club['name']) in response.data.decode()
        assert str(club['points']) in response.data.decode()

    assert response.status_code == 200