import calculate


user_name = input('Enter user name: ')
course = input('Enter course name: ')
quiz = int(input('Enter your quiz mark'))
lab = int(input('Enter your labs mark'))
assignment = int(input('Enter your assignments and project marks'))
presentation = int(input('Enter your presentation marks'))
participation = int(input('Enter your participation marks'))
midterm = int(input('Enter your midterm marks'))
final = int(input('Enter your final exam mark'))

print(calculate.calculate(user_name, course, quiz, lab, assignment, presentation, participation, midterm, final))

calculate.write_data()