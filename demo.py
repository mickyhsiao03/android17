import calculate

print("\n-------------------PASULATOR-------------------")
user_name = input('Enter user name: ')
course = input('Enter course name: ')
quiz = int(input('Enter your quiz mark: '))
lab = int(input('Enter your labs mark: '))
assignment = int(input('Enter your assignments and project marks: '))
presentation = int(input('Enter your presentation marks: '))
participation = int(input('Enter your participation marks: '))
midterm = int(input('Enter your midterm marks: '))
final = int(input('Enter your final exam mark: '))

grades = calculate.calculate(user_name, course, quiz, lab, assignment, presentation, participation, midterm, final)

print(f"\nYour final grade for {course} is {grades['total']}% ")

data = calculate.write_data(grades["user"], course, grades["quiz"], grades["lab"], grades["assignment"], 
    grades["presentation"], grades["participation"], grades["midterm"], grades["final"], grades["total"])
print(data)