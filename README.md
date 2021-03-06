# Financial Tracker
#### Video Demo:  https://youtu.be/r8jilGVrCz8
#### Description: This flask application is used for storing and tracking expenses, income and payments to help people with their finances.

## Technologies used:

* Python
* HTML
* CSS
* SQL Database
* Flask
* Jinja

## Requirements:

* CS50 Library [https://github.com/cs50/python-cs50](https://github.com/cs50/python-cs50)
* Flask [https://flask.palletsprojects.com/en/2.0.x/](https://flask.palletsprojects.com/en/2.0.x/)
* SQLITE3 [https://www.sqlite.org/index.html](https://www.sqlite.org/index.html)

## How to use this application:

1. install the above softwares using their guides.
2. Clone this repository 'git clone git@github.com:theguy404/CS50x-Final-Project.git'.
3. run command 'Flask run'.
4. open the link provided in the console inside a web browser.
5. register an account.
6. if successful this should land you on the main dashboard.

## Templates:

* layout.html - This file is the navigation bar design for each of the pages.
* index.html - This file hosts the main page of the site with 3 tables displaying expenses, income, transactions summaries.
* error.html - this file holds a template for any errors that the user will encounter on the site.
* expenses.html 
  * This file displays 2 tabs and a table below.
  * The first tab allows users to add expenses to their account.
  * The Second tab allows users to remove expenses from the account.
  * The table displays all current expenses in the account.
* income.html - this file is designed to act similar to expenses except is adds to the income table instead of expenses.
* transactions.html - This page allows the user to track payments they have made or money they have received and displays a history.
* login.html - this file is used to assist the user loging into their account.
* register.html - This page is designed to assist users wwith registering an account.

## Static:

* styles.css -  holds a few lines of style code to assist bootstrap with making the whole page look pretty!
* index.js -  holds 2 javascript functions to allow the tabs on each of the pages: expenses, income and transactions to work.

## Main Directory:

* application.py - this file is the main python file with all the logic for the page loading and template modification.
* helpers.py -  this was designed so act as python file to hold functions to assist the application.py file, currectly there is only one such function which acts and a login decorator.

## Future Additions:

* ability to remove transactions (in case of mistakes)
* ability to reset entire account data
* change color of expenses based on payments and late payments
* set automatic transactions for paychecks