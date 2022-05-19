import pytest 
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
    assert b'<link href="https://cdn.jsdelivr.net/npm/bootstrap-dark-5@1.1.3/dist/css/bootstrap-nightshade.min.css" rel="stylesheet">' in response.data


""" Unit test for "course search" function through dropdown menu """
def test_option(client):
    response = client.get("/option", query_string={"course_selection": "none"})
    assert b"Select a course!" in response.data
    assert response.status_code == 200

""" Unit test for calculate grade and update database """
def test_calculate_post(client):
    post_data = {
        "user": "test",
        "course_selection": "ACIT 1420",
        "quiz": 50,
        "lab": 100
    }
    response = client.post("/calculate_grade", data = post_data)
    assert response.status_code == 200
    
def test_dynamic_form(client):
    response = client.get("/option", query_string={"course_selection": "ACIT 1420"})
    assert response.status_code == 200

def test_gpa_results(client):
    results_response = client.post("/show_results", data ={"user": "micky"})
    gpa_response = client.post("/calculate_GPA", data ={"user": "micky"})
    assert results_response.status_code == 200
    assert gpa_response.status_code == 200