import json
import os 
import os.path
from datetime import date



def calculate(user_name, course, quiz, lab, assignment, presentation, participation, midterm, final):
    check_list = []
    with open("./courses.json" , 'r') as f:
        file_data = json.load(f)
        for courses in file_data:
            check_list.append(courses['course_name'])
        if course not in check_list:
            print('course not found')
            exit()
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

                    print('quiz mark:',quiz_mark,
                        'lab mark:', lab_mark,
                        'assignment mark:', assignment_mark,
                        'presentation mark:', presentation_mark,
                        'participation mark:', participation_mark,
                        'midterm mark:', midterm_mark,
                        'final mark:', final_mark,
                        'total mark:', total_mark
                    )
                    details = write_data(user_name, course, quiz_mark, lab_mark, assignment_mark, presentation_mark, participation_mark, midterm_mark, final_mark, total_mark)
                    return details

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
        with open("./users/{0}.json".format(user_name), 'r+') as f:
            file_data = json.load(f)
            file_data['course_name'] = course
            file_data['quiz'] = quiz_mark
            file_data['lab'] = lab_mark
            file_data['assignments_projects'] = assignment_mark
            file_data['presentations'] = presentation_mark
            file_data['participation'] = participation_mark
            file_data['midterm'] = midterm_mark
            file_data['final'] = final_mark
            file_data['total'] = total_mark
            file_data['date'] = today.strftime("%m/%d/%y")
            f.seek(0)
            json.dump(file_data, f, indent =4)
            f.truncate()
    else:
        with open("./users/{0}.json".format(user_name), 'r+') as f:
            file_data = json.load(f)
            file_data['course_name'] = course
            file_data['quiz'] = quiz_mark
            file_data['lab'] = lab_mark
            file_data['assignments_projects'] = assignment_mark
            file_data['presentations'] = presentation_mark
            file_data['participation'] = participation_mark
            file_data['midterm'] = midterm_mark
            file_data['final'] = final_mark
            file_data['total'] = total_mark
            file_data['date'] = today.strftime("%m/%d/%y")
            f.seek(0)
            json.dump(file_data, f, indent =4)
            f.truncate()
    return total_mark

        
