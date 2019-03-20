## Item Catalog Project
By Ayyappa Reddy Bareddy
This web app is a project for the Udacity Full Stack Nano Degree.


## About
This project is a web application and it is provides a list of items within a variety of categories as well as provide a user registration and authentication system. The Registered users will have the ability to post, modify, edit, and delete their own items.


## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels


## In This Project Main files
   1.In this project contains ac_main.py contains routes and json endpoints.
   2.db_setup.py contains the database models and tablenames it creates a database     file with table.
   3.db_init.py contains the sample data and insert into the database.
   
   
## Features
1. Checking the Proper authentication and authorisation.
2. Full CRUD support using Flask and SQLAlchemy.
3. Using the JSON endpoints.
4. Implements oAuth using with Google Sign-in API.


## Project Structure
--> _pycache_
       1. acs.db
	   2. acs.db-journal
	   3. db_setup.cpython-37.pyc
-->	static
       1. styles.css
-->	templates
	   1. AcTitles.html
       2. addAcBrand.html
       3. addAcDetails.html
       4. admin_login.html
       5. admin_loginFail.html
       6. allAcs.html
       7. deleteAc.html
       8. deleteAcCategory.html
       9. editAcCategory.html
      10. login.html
      11. mainpage.html
      12. myhome.html
      13. nav.html
      14. sample.html
      15. showAcs.html
--> venv
      1.Include
	  2.Lib
	  3.Scripts
	  4.tcl	  
--> ac_main
--> client_secrets.json
--> db_init.py
--> db_setup.py
--> README.md    	


## Steps to run this project
1. Download the Vagrant and then install the Vagrant.

2. Download the VirtualBox and then install VirtualBox.

3. Clone or download the Vagrant VM configuration file from here.

4. Open the above directory and navigate to the vagrant/ sub-directory.

5. Open terminal, and type

6. vagrant up
  This will cause Vagrant to download the Ubuntu operating system and install it. This may take quite a while depending on how fast your Internet connection is.

  After the above command succeeds, connect to the newly created VM by typing the following command:

7. vagrant ssh
  Type cd /vagrant/ to navigate to the shared repository.

8. Download or clone this repository, and navigate to it.

9. Install or upgrade Flask:

10. sudo python -m pip install --upgrade flask
    Run the following command to set up the database:

11. python db_setup.py
    Run the following command to insert dummy values. If you don't run this, the application will not run.

12. python db_init.py
    Run this application:

13. python ac_main.py
Open http://localhost:8000/ in your favourite Web browser, and enjoy.

14. Debugging
    In case the app doesn't run, make sure to confirm the following points:

15. You have run python db_init.py before running the application. This is an    essential step.

16. The latest version of Flask is installed.

17. The latest version of Python is installed.


## Known Issue
   This app might show an empty username if you sign in with a custom-domain-based Google account. For instance, if you use a Google account bareddyayyappareddy123@gmail.com, this app might show an empty username. So, make sure to use an email with gmail.com domain only for best experience.
 
## Help and Support
   In case you run into any trouble, create an issue on GitHub. I will make sure to look into it as soon as possible.

