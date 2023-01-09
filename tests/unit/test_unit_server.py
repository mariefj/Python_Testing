import pytest
from datetime import datetime

def test_showSummary_success(client, clubs_data):
    club = clubs_data[0]

    response = client.post('/showSummary', data={'email': club['email']})

    assert response.status_code == 200

def test_showSummary_club_not_found(client, clubs_data):
    response = client.post('/showSummary', data={'email': 'invalid@example.com'})

    assert response.status_code == 404
    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, this email wasn't found."


def test_book_success(client, clubs_data, competitions_data):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')

    assert response.status_code == 200

def test_book_club_not_found(client, clubs_data, competitions_data):
    competition = competitions_data[0]
    response = client.get(f'/book/{competition["name"]}/ClubD')

    assert response.status_code == 404
    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, something went wrong. Please try again"

def test_book_competition_not_found(client, clubs_data, competitions_data):
    club = clubs_data[0]
    response = client.get(f'/book/Competition4/{club["name"]}')

    assert response.status_code == 404
    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, something went wrong. Please try again"

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

    assert b'Sorry, this competition is over' in response.data