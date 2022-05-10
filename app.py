import json
from flask import Flask, render_template, request, jsonify, flash
from calculate import *

app = Flask(__name__)
app.secret_key = "secret"

courses_list = []
with open("courses.json") as file:
    data = json.load(file)
for i in data:
    courses_list.append(i["course_name"])

@app.route("/")
def homepage():
    return render_template("index.html", courses=courses_list)

@app.route("/option", methods = ['GET'])
def option():
    returned_form = ""
    selected_course = request.args["course_selection"]
    if selected_course == "none":
        return "Select a course!"
    else:
        for course_dict in data:
            if course_dict["course_name"] == selected_course:
                for key in course_dict:
                    if (course_dict[key] != 0) and (key != "credit") and (key != "course_name"):
                        returned_form += f"<div class='form-group'><input type='number' name='{key}' placeholder='{key}' class='form-control' />"
                return returned_form

@app.route("/calculate_grade", methods = ["POST"])
def calculate_post():
    try:
        quiz = int(request.form["quiz"])
    except KeyError:
        quiz = 0
    try:
        lab = int(request.form["lab"])
    except KeyError:
        lab = 0
    try:
        assignments = int(request.form["assignments_projects"])
    except KeyError:
        assignments = 0
    try:
        presentations = int(request.form["presentations"])
    except KeyError:
        presentations = 0
    try:
        participation = int(request.form["participation"])
    except KeyError:
        participation = 0
    try:
        midterm = int(request.form["midterm"])
    except KeyError:
        midterm = 0
    try:
        final = int(request.form["final"])
    except KeyError:
        final = 0

    final_calculated_grade = calculate(
        "nikola",
        request.form["course_selection"],
        quiz,
        lab,
        assignments,
        presentations,
        participation,
        midterm,
        final
    )
    
    flash(f"Your final grade for {request.form['course_selection']} is {final_calculated_grade['total']}")
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)
