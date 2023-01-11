import pytest


##########################  app success  ###############################


def test_app_success(client, clubs_data, competitions_data, cart):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.get('/')
    assert 'Welcome to the GUDLFT Registration' in response.data.decode()

    response = client.post('/showSummary', data={'email': club['email']})
    assert response.status_code == 200

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    assert response.status_code == 200
    assert str(club['name']) in response.data.decode()

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 10,
    })
    assert response.status_code == 200

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 2,
    })
    assert cart[competition['name']][club['name']] == 12
    assert response.status_code == 200

    response = client.get('/logout')
    assert response.headers["Location"] == "http://localhost/"


##########################  app fail purchasePlaces  ###############################


def test_app_fail_to_book_more_than_maxPlaces(client, clubs_data, competitions_data, cart):
    club = clubs_data[0]
    competition = competitions_data[0]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 50,
    })
    assert response.status_code == 400

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 5,
    })
    assert response.status_code == 200

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 5,
    })
    assert response.status_code == 200

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 5,
    })
    assert response.status_code == 400

    assert cart[competition['name']][club['name']] == 10

