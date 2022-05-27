# Passulator
## CIT Course Grade & GPA Calculator
### ACIT 2911 - Agile Development Project
![Application Logo](/static/images/logo.png)

* Project Description
  - Calculates the user's course grades using grade distributions from CIT courses
  - Also provides functionality to calculate GPA 
  - Users can view results in a JSON table or download a text file with their calculated grades  

* Project Purpose
  - The project is useful for BCIT CIT students because all the grade distributions are stored into the database. Students who are using our grade calculator do not need to manually  search through D2L to calculate their grade. 

* Project Contributors:
  - Dennis Phan (dphan12@my.bcit.ca)
  - Shih Chieh (Micky) Hsiao (mhsiao6@my.bcit.ca)
  - Pin Chien (Patrick) Ho (pho85@my.bcit.ca)
  - Nikola Velinov (nvelinov@my.bcit.ca)
  - Byeongju (Jace) Kang (jkang86@my.bcit.ca)
  - Aashay Bharadwaj (abharadwaj1@my.bcit.ca)

* How to run the app locally?
  - Clone the repo:
   `git clone https://github.com/mickyhsiao03/android17`
  - Change into the repo directory:
   `cd android17/`
  - Install dependencies:
   `pip install -r requirements.txt`
  - Run the app:
   `python app.py`
  - Navigate to the app URL: `localhost:6969` 

* How can users get started with the project?
  - First, enter your username
  - Then, select a course to calculate grades for
  - Input your percentage for each category of the course weight
  - Calculate the grade by clicking on the calculate grade button
  - View your results by clicking the view results button
  - Press calculate GPA to calculate your GPA
  - Download a file using the download grades button
  - Additionally, you can switch to light mode or dark mode using the toggle at the top of the screen

* Startup & Deployment 
  - Application is deployed to Microsoft Azure app services. Simply select and start the application in the console page to browse the application on a secure URL.

* Continuous Integration
  - Continuous Integration is enabled for the repository. Unit tests will trigger on push to the main branch to ensure code functionality and quality.

* Continuous Deployment
  - Continuous Deployment is enabled for the repository. This app is deployed to Microsoft Azure app services. When a change is pushed to the main branch, it will automatically redeploy the application with the changes.

* Technologies Used 
 	- Boostrap (https://getbootstrap.com/)
	- HTMX (https://htmx.org/)
	- Bootstrap dark mode addon (https://vinorodrigues.github.io/bootstrap-dark-5/)
	- Python Flask (https://flask.palletsprojects.com/en/2.1.x/)
	- Pytest (https://docs.pytest.org/en/7.1.x/)


