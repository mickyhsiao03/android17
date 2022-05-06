import pytest
from datetime import date

from calculate import *
from unittest.mock import mock_open, patch


USER_JSON = """ [
    {
        "course_name": "",
        "quiz": 0,
        "lab": 0,
        "assignments_projects": 0,
        "presentations": 0,
        "participation": 0,
        "midterm": 0,
        "final": 0,
        "total": 0,
        "date": ""
    }
]"""

COURSE_JSON = """[
    {
        "course_name": "ACIT 1420",
        "quiz": 15,
        "lab": 20,
        "assignments_projects": 0,
        "presentations": 10,
        "participation": 15,
        "midterm": 15,
        "final": 25,
        "credit": 4
    }
]"""

@pytest.fixture
@patch("builtins.open", new_callable=mock_open, read_data=COURSE_JSON)
def grades(mock_file):
    return calculate("Nikola", "ACIT 1420", 100, 80, 0, 70, 90, 70, 80)

@patch("builtins.open", new_callable=mock_open, read_data=COURSE_JSON)
def test_calculate(mock_file, grades):
    
    grades = calculate("Nikola", "ACIT 1420", 100, 80, 0, 70, 90, 70, 80)
    assert grades["user"] == "Nikola"
    assert grades["quiz"] == 15
    assert grades["lab"] == 16
    assert grades["assignment"] == 0
    assert grades["presentation"] == 7
    assert grades["participation"] == 13.5
    assert grades["midterm"] == 10.5
    assert grades["final"] == 20
    assert grades["total"] == 82
    
    assert mock_file.call_count == 1
    assert mock_file.call_args[0][0] == "./courses.json"
    assert mock_file.assert_called_once_with("./courses.json", "r") is None

@patch("builtins.open", new_callable=mock_open, read_data=COURSE_JSON)
def test_calculate_invalid(mock_file):
    with pytest.raises(FileNotFoundError):
        calculate("Nikola", "ACIT 16630", 0, 0, 0, 0, 0, 0, 0)
    with pytest.raises(ValueError):
        calculate("Nikola", "", 0, 0, 0, 0, 0, 0, 0)
    with pytest.raises(ValueError):
        calculate("Nikola", "Velinov", 0, 0, -1, 0, 0, 0, 0)
    with pytest.raises(ValueError):
        calculate("Nikola", "Velinov", 0, 0, 0, 0, 101, 0, 0)

@patch("json.dump")
@patch("json.load")
@patch("builtins.open", new_callable=mock_open)
def test_update_json_file(mock_file, mock_json, grades):
    update_json_file(
        "Nikola", 
        date.today(),
        "ACIT 1420", 
        grades["quiz"], 
        grades["lab"],
        grades["assignment"], 
        grades["presentation"], 
        grades["participation"], 
        grades["midterm"], 
        grades["final"], 
        grades["total"]
    )

    assert mock_file.call_count == 1
    assert mock_file.call_args[0][0] == './users/Nikola.json'
    assert mock_file.assert_called_once_with('./users/Nikola.json', 'r+') is None

@patch("os.path.exists", return_value = False)
@patch("json.load")
@patch("json.dump")
@patch("builtins.open", new_callable=mock_open, read_data=USER_JSON)
def test_write_data(mock_file, mock_json, mock_os, grades):
    result = write_data(
        "Nikola", 
        "ACIT 1420", 
        grades["quiz"], 
        grades["lab"],
        grades["assignment"], 
        grades["presentation"], 
        grades["participation"], 
        grades["midterm"], 
        grades["final"], 
        grades["total"]
    )
    assert result == 'JSON Created & Updated' 

@patch("os.path.exists", return_value = True)
@patch("json.load")
@patch("json.dump")
@patch("builtins.open", new_callable=mock_open, read_data=USER_JSON)
def test_write_data_exists(mock_file, mock_json, mock_os, grades):
    result = write_data(
        "Nikola", 
        "ACIT 1420", 
        grades["quiz"], 
        grades["lab"],
        grades["assignment"], 
        grades["presentation"], 
        grades["participation"], 
        grades["midterm"], 
        grades["final"], 
        grades["total"]
    )
    assert result == "JSON successfully updated" 

