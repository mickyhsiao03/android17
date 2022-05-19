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

    blank_dict = {
        "quiz": 0,
        "lab": 0,
        "assignments_projects": 0,
        "presentations": 0,
        "participation": 0,
        "midterm": 0,
        "final": 0
    }

    for key in request.form.keys():
        if key != "course_selection" and key !="user":
            blank_dict[key] = float(request.form[key])


    final_calculated_grade = calculate(
        request.form["user"],
        request.form["course_selection"],
        blank_dict["quiz"],
        blank_dict["lab"],
        blank_dict["assignments_projects"],
        blank_dict["presentations"],
        blank_dict["participation"],
        blank_dict["midterm"],
        blank_dict["final"]
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

#CI testing