import json
import os 
import os.path
from datetime import date

def calculate_GPA(user_name):
    with open("./users/{0}.json".format(user_name), 'r+') as f:
        file_data = json.load(f)
        earned_list = {}
        for i in file_data:
            if i['total'] >= 50:
                earned_list[i['course_name']] = i['total']
    with open("courses.json", 'r') as f:
        file_data = json.load(f)
        grades = []
        credits = []
        for course in file_data:
            for i in earned_list:
                if course['course_name'] == i:
                    credits.append(course['credit'])
                    grades.append(course['credit']*earned_list[i])
    GPA = sum(grades)/sum(credits)
    return GPA

def get_course_by_name(course):
    with open("courses.json") as f:
        data = json.load(f)
    for i in data:
        if i['course_name'] == course:
            return i


def get_all_courses():
    with open("courses.json") as file:
        data = json.load(file)
    return [i["course_name"] for i in data]


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
    if course not in get_all_courses():
        raise FileNotFoundError
    else:
        course_dict = get_course_by_name(course)
        quiz_mark = quiz * (course_dict['quiz']/100)
        lab_mark = lab * (course_dict['lab']/100)
        assignment_mark = assignment * (course_dict['assignments_projects']/100)
        presentation_mark = presentation * (course_dict['presentations']/100)
        participation_mark = participation * (course_dict['participation']/100)
        midterm_mark = midterm * (course_dict['midterm']/100)
        final_mark = final * (course_dict['final']/100)
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


#called
def update_json_file(username, today, course, quiz, lab, assignment, presentation, participation, midterm, final, total):
    with open(f"./users/{username}.json", 'r+') as file:
        data = json.load(file)
        user_list = [i['course_name'] for i in data]
        for i in data:
            if i['course_name']=="":
                for i in data:
                    i["course_name"] = course
                    i["quiz"] = quiz
                    i["lab"] = lab
                    i["assignments_projects"] = assignment
                    i["presentations"] = presentation
                    i["participation"] = participation
                    i["midterm"] = midterm
                    i["final"] = final
                    i["total"] = total
                    i["date"] = today.strftime("%m/%d/%y")
                    file.seek(0)
                    json.dump(data, file, indent =4)
                    file.truncate()
                return data

        if course not in user_list:
            values = [course, quiz, lab, assignment, presentation, participation, midterm, final, round(total,2), today.strftime("%m/%d/%y")]
            keys = ["course_name", "quiz", "lab", "assignments_projects", "presentations", "participation", "midterm", "final", "total", "date"]
            data.append(dict(zip(keys, values)))
            file.seek(0)
            json.dump(data, file, indent =4)
            file.truncate()
        else:
            for i in data:
                if i['course_name'] == course:
                    i['quiz'] = quiz
                    i['lab'] = lab
                    i['assignments_projects'] = assignment
                    i['presentations'] = presentation
                    i['participation'] = participation
                    i['midterm'] = midterm
                    i['final'] = final
                    i['total'] = round(total,2)
                    i['date'] = today.strftime("%m/%d/%y")
                    file.seek(0)
                    json.dump(data, file, indent =4)
                    file.truncate()

        return data


def write_data(user_name, course, quiz_mark, lab_mark, assignment_mark, presentation_mark, participation_mark, midterm_mark, final_mark, total_mark):
    today = date.today()
    if not os.path.exists("./users/{0}.json".format(user_name)):
        create_json = [{
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
                        }]
        with open("./users/{0}.json".format(user_name), 'w') as f:
            json.dump(create_json, f, indent=4)
        update_json_file(user_name, today, course, quiz_mark, lab_mark, assignment_mark, 
        presentation_mark, participation_mark, midterm_mark, final_mark, total_mark)
        return "JSON Created & Updated"
    else:
        update_json_file(user_name, today, course, quiz_mark, lab_mark, assignment_mark, 
        presentation_mark, participation_mark, midterm_mark, final_mark, total_mark)

    return "JSON successfully updated"
