import pytest 
from flask import Flask
import os
import tempfile
from app import *


""" Unit test for app=Flask(__name__) to start Flask """
@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


""" Unit test for homepage, expect our app to display bootstrap """
def test_homepage(client):
    response = client.get("/")
    assert b'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">' in response.data


""" Unit test for "course search" function through dropdown menu """
def test_option(client):
    response = client.get("/option")
    assert b"Select a course!" in response.data
    assert response.status_code == 200

""" Unit test for calculate grade and update database """
def test_calculate_post(client):
    response = client.post("/calculate_grade")
    assert response.status_code == 200
    