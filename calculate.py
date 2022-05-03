import json
import os 
import os.path
from datetime import date

user_name = input('enter a user name: ')


def calculate(course, quiz, lab, assignment, presentation, participation, midterm, final):
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
                   # details = write_data(user_name, course, quiz_mark, lab_mark, assignment_mark, presentation_mark, participation_mark, midterm_mark, final_mark, total_mark)
                    return 
 
            
