import pytest
import server


@pytest.fixture
def client(monkeypatch, clubs_data, competitions_data, cart):
    monkeypatch.setattr(server, 'clubs', clubs_data)
    monkeypatch.setattr(server, 'competitions', competitions_data)
    monkeypatch.setattr(server, 'cart', cart)
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def clubs_data():
    return [{
        'name': 'Club A',
        'email': 'cluba@example.com',
        'points': 20
    }, {
        'name': 'Club B',
        'email': 'clubb@example.com',
        'points': 10
    }, {
        'name': 'Club C',
        'email': 'clubc@example.com',
        'points': 5
    }]

@pytest.fixture
def competitions_data():
    return [{
        'name': 'Competition 1',
        'date': '2023-02-01 10:00:00',
        'numberOfPlaces': 30
    }, {
        'name': 'Competition 2',
        'date': '2023-02-02 09:00:00',
        'numberOfPlaces': 7
    }, {
        'name': 'Competition 3',
        'date': '2023-01-02 09:00:00',
        'numberOfPlaces': 12
    }]

@pytest.fixture
def cart(clubs_data, competitions_data):
    return {
        competition["name"]: {club["name"]: 0 for club in clubs_data}
        for competition in competitions_data
    }

@pytest.fixture
def competition_over(competitions_data):
    competitions_data[0]["date"] = "2022-02-01 10:00:00"
    return competitions_data[0]