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
    response = client.get('/book/Competition4/ClubD')

    assert response.status_code == 404
    with pytest.raises(Exception) as e:
        assert e.value == "Sorry, this competition wasn't found."