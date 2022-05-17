from flask import Flask, render_template, request, jsonify, flash, send_from_directory
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
    global username
    username = request.form['user']
    blank_dict = dict.fromkeys(["quiz", "lab", "assignments_projects", "presentations", "participation", "midterm", "final"], 0)

    for key in request.form.keys():
        if key != "course_selection" and key !="user":
            blank_dict[key] = float(request.form[key])

    final_calculated_grade = calculate(request.form["user"],request.form["course_selection"],**blank_dict)
    
    write_data(**final_calculated_grade,course=request.form["course_selection"])
    
    return (f"<div class='alert alert-primary mb-3 mt-3' role='alert'> Your final grade for {request.form['course_selection']} is {int(final_calculated_grade['total'])}% </div>")


@app.route("/show_results", methods = ["POST"])
def results():
    try:
        global username
        username = request.form['user']
        with open(f"./users/{request.form['user']}.json") as file:
            data = json.load(file)
            data.sort(key=lambda x:x["total"], reverse=True)
        returned_table = "<table class='table'>"
        returned_table += "<thead><tr><th scope='col'>Course</th><th scope='col'>Final Grade</th><th scope='col'>Date Calculated</th></tr></thead>"
        returned_table += "<tbody>"
        for i in data:
            returned_table += f"<tr><td>{i['course_name']}</td"
            returned_table += f"<tr><td>{i['total']}%</td>"
            returned_table += f"<td>{i['date']}</td></tr>"
        returned_table += " </tbody></table>"
        return returned_table
    except FileNotFoundError:
        return "<h4>Please enter a valid username.</h4><h6 class='text-muted'>Please ensure there is at least one grade calculation for your username.</h6>"

@app.route("/download_file", methods = ["POST", "GET"])
def create_download_file():
    try:
        global username
        print(username)
        f = open('./users/{0}.json'.format(username), "r")
        data = json.load(f)
        with open('./static/download/{0}.txt'.format(username), 'w') as f:
            for i in data:
                f.write("Course Name: "+ i["course_name"] + "\n" + "Quiz: "+ str(i["quiz"])+ "\n" + "Lab: " + str(i["lab"])+ "\n" + "Assignment Projects: "+ str(i["assignments_projects"])+ "\n"+ "Presentations: "+ str(i["presentations"])+ "\n"
                        "Participation: "+ str(i["participation"])+ "\n" + "Midterm: " + str(i["midterm"]) + "\n" + "Final: " + str(i["final"]) + "\n" + "Date Calculated: " + str(i["date"]) + "\n \n \n \n")
        filename = '{0}.txt'.format(username)
        # simp_path = 'demo/which_path.docx'
        abs_path = os.path.abspath("./static/download")
        print(abs_path)
        username = ''
        return send_from_directory(abs_path, filename, as_attachment=True)  
    except:
        message = flash ("Please Check Grade History or Calculate Grades at least once!")
        return render_template("index.html", courses=get_all_courses()) 

if __name__ == "__main__":
    app.run(port=6969,debug=True)
