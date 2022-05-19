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

UPDATED_JSON = """[
    {
        "course_name": "ACIT 1420",
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

GPA_JSON = """
[
    {
        "course_name": "ACIT 1420",
        "quiz": 7.5,
        "lab": 20.0,
        "assignments_projects": 0.0,
        "presentations": 0.0,
        "participation": 0.0,
        "midterm": 0.0,
        "final": 0.0,
        "total": 27.5,
        "date": "05/18/22",
        "credit": 4
    },
    {
        "course_name": "MATH 1310",
        "quiz": 7.5,
        "lab": 6.75,
        "assignments_projects": 12.0,
        "presentations": 0.0,
        "participation": 0.0,
        "midterm": 30.0,
        "final": 36.0,
        "total": 92.25,
        "date": "05/14/22",
        "credit": 4
    }
]

"""



@pytest.fixture
@patch("builtins.open", new_callable=mock_open, read_data=COURSE_JSON)
def grades(mock_file):
    return calculate("Nikola", "ACIT 1420", 100, 80, 0, 70, 90, 70, 80)

def test_calculate(grades):
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


@patch("builtins.open", new_callable=mock_open, read_data=COURSE_JSON)
def test_get_course_by_name(mock_file):
    result = get_course_by_name("ACIT 1420")
    assert result["quiz"] == 15
    assert result["lab"] == 20
    assert result["assignments_projects"] == 0
    assert result["presentations"] == 10
    assert result["participation"] == 15
    assert result["midterm"] == 15
    assert result["final"] == 25
    assert result["credit"] == 4

@patch("builtins.open", new_callable=mock_open, read_data=COURSE_JSON)
def test_get_all_courses(mock_file):
    assert get_all_courses() == ["ACIT 1420"]

@patch("builtins.open", new_callable=mock_open, read_data=USER_JSON)
def test_multiple_stored_results(mock_file):
    #Doesnt matter for this test what the numbers are, just that there are multiple course items in the json file
    result = update_json_file("nikola", date(2022, 5, 12), "ACIT 1620", 1, 1, 1, 1, 1, 1, 1, 7)
    assert result[0]["quiz"] == 1
    assert result[0]["lab"] == 1
    assert result[0]["assignments_projects"] == 1
    assert result[0]["presentations"] == 1  
    assert result[0]["participation"] == 1
    assert result[0]["midterm"] == 1   
    assert result[0]["final"] == 1
    assert result[0]["total"] == 7
    assert result[0]["date"] == "05/12/22"

    updated_dict = {
        "course_name": "ACIT 1420",
        "quiz": 1,
        "lab": 1,
        "assignments_projects": 1,
        "presentations": 1,
        "participation": 1,
        "midterm": 1,
        "final": 1,
        "total": 1,
        "date": "05/12/22"
    }


    result = update_json_file("Nikola", date(2022, 5, 12),"ACIT 1420", 1, 1,1, 1, 1, 1, 1, 1)

    assert result[0] == updated_dict
    
@patch("builtins.open", new_callable=mock_open, read_data=UPDATED_JSON)
def test_update_existing_course(mock_file):    

    result = update_json_file("nikola", date(2022, 5, 12), "ACIT 1420", 1, 1, 1, 1, 1, 1, 1, 7)


    assert result[-1]["quiz"] == 1
    assert result[-1]["lab"] == 1
    assert result[-1]["assignments_projects"] == 1
    assert result[-1]["presentations"] == 1  
    assert result[-1]["participation"] == 1
    assert result[-1]["midterm"] == 1   
    assert result[-1]["final"] == 1
    assert result[-1]["total"] == 7
    assert result[-1]["date"] == "05/12/22"


@patch("builtins.open", new_callable=mock_open, read_data=GPA_JSON)
def test_calculate_gpa(mock_file):
    assert calculate_GPA("test") == 46.125

@patch("builtins.open", new_callable=mock_open, read_data=GPA_JSON)
def test_delete_entry(mock_file):
    assert delete_entry("test", "ACIT 1420") == "ACIT 1420 has been deleted for test"
    assert delete_entry("test", "MATH 1350") == "MATH 1350 has been deleted for test"