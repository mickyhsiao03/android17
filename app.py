from flask import Flask, render_template, request, send_from_directory, Response, url_for
from calculate import *
import json

app = Flask(__name__)

formatting_dict = {
    "course_name": "Course Name",
    "quiz": "Quiz",
    "lab": "Lab",
    "assignments_projects": "Assignments & Projects",
    "presentations": "Presentations",
    "participation": "Participation",
    "midterm": "Midterm",
    "final": "Final",
    "total": "Total Grade",
    "date": "Date Calculated"
}

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
                returned_form += f"<div class='mb-3 mt-3'><input type='number' step='0.01' min=0 max=100 name='{key}' placeholder='{formatting_dict[key]}' class='form-control'/>"
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
    except ZeroDivisionError:
        return (f"<h4>There are no grades stored for {request.form['user']}</h4> ")
    


@app.route("/show_results", methods = ["POST"])
def results():
    try:
        with open(f"./users/{request.form['user']}.json") as file:
            data = json.load(file)
            data.sort(key=lambda x:x["total"], reverse=True)
        returned_table = ""
        returned_table += f"<button class='btn btn-primary mb-1 mt-1' hx-get='{url_for('downloadredir')}' hx-include=\"[name='user']\">Download Grades</button>"
        returned_table += "<table class='table'>"
        returned_table += "<thead><tr><th scope='col'>Course</th><th scope='col'>Final Grade</th><th scope='col'>Date Calculated</th><th scope='col'></th></tr></thead>"
        returned_table += "<tbody>"
        for i in data:
            returned_table += f"<tr id='{i['course_name']}'><td>{i['course_name']}</td>"
            returned_table += f"<td>{i['total']}%</td>"
            returned_table += f"<td>{i['date']}</td>"
            returned_table += f"<td><button hx-target='#json' class='btn btn-primary mb-1 mt-1' onclick=\"delete_entry('{request.form['user']}','{i['course_name']}')\" >Delete</button><td></tr>"
        returned_table += "</tbody></table>"
        return returned_table
    except FileNotFoundError:
        return "<h4>Please enter a valid username.</h4><h6 class='text-muted'>Please ensure there is at least one grade calculation for your username.</h6>"


@app.route("/downloadredir", methods = ["GET"])
def downloadredir():
    return Response(headers={"HX-Redirect": f"/download_file?user={request.args['user']}"})

@app.route("/download_file", methods = ["GET"])
def create_download_file():
        username = request.args["user"]
        f = open(f'./users/{username}.json', "r")
        data = json.load(f)
        with open('./static/download/{0}.txt'.format(username), 'w') as f:
            for i in data:
                to_write = ""
                to_write += ("----------------------------------------")
                for key in i:
                    if i[key] != 0:
                        to_write += f"\n{formatting_dict[key]}: {str(i[key])}"
                        if type(i[key]) is float:
                            to_write += "%"
                to_write += "\n----------------------------------------\n\n"
                f.write(to_write)

        filename = f'{username}.txt'
        abs_path = os.path.abspath("./static/download")
        return send_from_directory(abs_path, filename, as_attachment=True)  

@app.route("/delete_entry", methods=["POST"])
def delete_item():
    req_list = request.data.decode("utf-8").split(",")
    delete_entry(req_list[0],req_list[1])
    return f'deleted {req_list[1]} for {req_list[0]}'


if __name__ == "__main__":
    app.run(port=6969,host='0.0.0.0')

#CI testing