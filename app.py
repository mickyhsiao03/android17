from flask import Flask, render_template, request, jsonify
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
                returned_form += f"<div class='form-text'>Weight = {course_dict[key]}%</div>"
        return returned_form

@app.route("/calculate_grade", methods = ["POST"])
def calculate_post():

    try:
        blank_dict = dict.fromkeys(["quiz", "lab", "assignments_projects", "presentations", "participation", "midterm", "final"], 0)

        for key in request.form.keys():
            if key != "course_selection" and key !="user":
                blank_dict[key] = float(request.form[key])

        final_calculated_grade = calculate(request.form["user"],request.form["course_selection"],**blank_dict)
        
        write_data(**final_calculated_grade,course=request.form["course_selection"])
        


        return (f"<div class='alert alert-primary mb-3 mt-3' role='alert'> Your final grade for {request.form['course_selection']} is {int(final_calculated_grade['total'])}% </div>")
    except (ValueError, FileNotFoundError):
        return "<h4>Please enter a valid username.</h4><h6 class='text-muted'>Please ensure there is at least one grade calculation for your username.</h6>"


@app.route("/calculate_GPA", methods = ["POST"])
def calculate_GPA_form():
    try:
        GPA = calculate_GPA(request.form["user"])
        return(f"<div class='alert alert-primary mb-3 mt-3' role='alert'> Your GPA for your saved courses is {round(GPA,2)}% </div>")
    except FileNotFoundError:
        return "<h4>Please enter a valid username.</h4><h6 class='text-muted'>Please ensure there is at least one grade calculation for your username.</h6>"
    


@app.route("/show_results", methods = ["POST"])
def results():
    try:
        with open(f"./users/{request.form['user']}.json") as file:
            data = json.load(file)
            data.sort(key=lambda x:x["total"], reverse=True)
        returned_table = "<table class='table'>"
        returned_table += "<thead><tr><th scope='col'>Course</th><th scope='col'>Final Grade</th></tr></thead>"
        returned_table += "<tbody>"
        for i in data:
            returned_table += f"<tr><td>{i['course_name']}</td>"
            returned_table += f"<td>{i['total']}%</td></tr>"
        returned_table += " </tbody></table>"
        return returned_table
    except FileNotFoundError:
        return "<h4>Please enter a valid username.</h4><h6 class='text-muted'>Please ensure there is at least one grade calculation for your username.</h6>"

#TESTING
if __name__ == "__main__":
    app.run(port=6969,debug=True)
