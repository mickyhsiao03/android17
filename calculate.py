import json
import os 
import os.path
from datetime import date

def validate(*args):
    for i in args[0]:
        if type(i) is str:
            if i == "":
                raise ValueError
        if type(i) is int:
            if (i > 100) or (i < 0):
                raise ValueError

def calculate(user_name, course, quiz, lab, assignment, presentation, participation, midterm, final):
    validate([i for i in locals().values()])
    check_list = []
    with open("./courses.json" , 'r') as f:
        file_data = json.load(f)
        for courses in file_data:
            check_list.append(courses['course_name'])
        if course not in check_list:
            raise FileNotFoundError
        else:
            for i in file_data:
                if i['course_name'] == course:
                    quiz_mark = quiz * (i['quiz']/100)
                    lab_mark = lab * (i['lab']/100)
                    assignment_mark = assignment * (i['assignments_projects']/100)
                    presentation_mark = presentation * (i['presentations']/100)
                    participation_mark = participation * (i['participation']/100)
                    midterm_mark = midterm * (i['midterm']/100)
                    final_mark = final * (i['final']/100)
                    total_mark = quiz_mark + lab_mark + assignment_mark + presentation_mark + participation_mark + midterm_mark +final_mark

                    return {
                        'user': user_name,
                        'quiz': quiz_mark,
                        'lab': lab_mark,
                        'assignment': assignment_mark,
                        'presentation': presentation_mark,
                        'participation': participation_mark,
                        'midterm': midterm_mark,
                        'final': final_mark,
                        'total': total_mark
                    }

def update_json_file(username, date, course, quiz, lab, assignment, presentation, participation, midterm, final, total):
    with open("./users/{0}.json".format(username), 'r+') as file:
        data = json.load(file)
        data["course_name"] = course
        data["quiz"] = quiz
        data["lab"] = lab
        data["assignments_projects"] = assignment
        data["presentations"] = presentation
        data["participation"] = participation
        data["midterm"] = midterm
        data["final"] = final
        data["total"] = total
        data["date"] = date
        file.seek(0)
        json.dump(data, file, indent =4)
        file.truncate()
        return data

def write_data(user_name, course, quiz_mark, lab_mark, assignment_mark, presentation_mark, participation_mark, midterm_mark, final_mark, total_mark):
    today = date.today()
    if not os.path.exists("./users/{0}.json".format(user_name)):
        create_json = {
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
        with open("./users/{0}.json".format(user_name), 'w') as f:
            json.dump(create_json, f, indent=4)
        update_json_file(user_name, today, course, quiz_mark, lab_mark, assignment_mark, 
        presentation_mark, participation_mark, midterm_mark, final_mark, total_mark)
        return "JSON Created & Updated"
    else:
        update_json_file(user_name, today, course, quiz_mark, lab_mark, assignment_mark, 
        presentation_mark, participation_mark, midterm_mark, final_mark, total_mark)

    return "JSON successfully updated"
