from flask import Flask, render_template, request
from calculate import *

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def homepage():
    return render_template("index.html", courses=get_all_courses())

@app.route("/option", methods = ['GET'])
def option():
    returned_form = ""
    selected_course = request.args["course_selection"]
    if selected_course == "none":
        return "Select a course!"
    else:
        course_dict = get_course_by_name(selected_course)
        for key in course_dict:
            if (course_dict[key] != 0) and (key != "credit") and (key != "course_name"):
                returned_form += f"<div class='mb-3 mt-3'><input type='number' step='0.01' min=0 max=100 name='{key}' placeholder='{key}' class='form-control'/>"
                returned_form += f"<div class='form-text' style='color:black;'>Weight = {course_dict[key]}%</div>"
        return returned_form

@app.route("/calculate_grade", methods = ["POST"])
def calculate_post():
    try:
        quiz = float(request.form["quiz"])
    except KeyError:
        quiz = 0
    try:
        lab = float(request.form["lab"])
    except KeyError:
        lab = 0
    try:
        assignments = float(request.form["assignments_projects"])
    except KeyError:
        assignments = 0
    try:
        presentations = float(request.form["presentations"])
    except KeyError:
        presentations = 0
    try:
        participation = float(request.form["participation"])
    except KeyError:
        participation = 0
    try:
        midterm = float(request.form["midterm"])
    except KeyError:
        midterm = 0
    try:
        final = float(request.form["final"])
    except KeyError:
        final = 0

    final_calculated_grade = calculate(
        "micky",
        request.form["course_selection"],
        quiz,
        lab,
        assignments,
        presentations,
        participation,
        midterm,
        final
    )

    write_data(
        final_calculated_grade['user'], 
        request.form["course_selection"],
        final_calculated_grade['quiz'],
        final_calculated_grade['lab'],
        final_calculated_grade['assignment'],
        final_calculated_grade['presentation'],
        final_calculated_grade['participation'],
        final_calculated_grade['midterm'],
        final_calculated_grade['final'],
        final_calculated_grade['total']
    )
    
    return (f"<div class='alert alert-primary mb-3 mt-3' role='alert'> Your final grade for {request.form['course_selection']} is {int(final_calculated_grade['total'])}% </div>")

if __name__ == "__main__":
    app.run(port=6969,debug=True)
