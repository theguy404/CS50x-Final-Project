import datetime
from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from cs50 import SQL

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")


@app.route("/")
@login_required
def index():
    
    # query the database for all expenses saves to users account
    expenseItems = db.execute("SELECT * FROM expenses WHERE user_id = ?;", session.get("user_id"))
    
    # get total amount of expenses
    expTotal = 0
    for i in range(len(expenseItems)):
        if expenseItems[i]['frequency'] == "Weekly":
            expTotal += expenseItems[i]['amount'] * 4
        if expenseItems[i]['frequency'] == "Bi-Weekly":
            expTotal += expenseItems[i]['amount'] * 2
        if expenseItems[i]['frequency'] == "Monthly":
            expTotal += expenseItems[i]['amount']
        if expenseItems[i]['frequency'] == "Yearly":
            expTotal += expenseItems[i]['amount'] / 12
    
    # query the database for all income saves to users account
    incomeItems = db.execute("SELECT * FROM income WHERE user_id = ?;", session.get("user_id"))
    
    # get total amount of income
    incTotal = 0
    for i in range(len(incomeItems)):
        if incomeItems[i]['frequency'] == "Weekly":
            incTotal += incomeItems[i]['amount'] * 4
        if incomeItems[i]['frequency'] == "Bi-Weekly":
            incTotal += incomeItems[i]['amount'] * 2
        if incomeItems[i]['frequency'] == "Monthly":
            incTotal += incomeItems[i]['amount']
        if incomeItems[i]['frequency'] == "Yearly":
            incTotal += incomeItems[i]['amount'] / 12
    
    # query the database for all transactions saved to users account
    transItems = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY trans_id DESC LIMIT 10;", session.get("user_id"))
    
    return render_template("index.html",
                           expenseItems=expenseItems, 
                           incomeItems=incomeItems, 
                           transItems=transItems, 
                           expTotal=expTotal,
                           incTotal=incTotal)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error="Missing username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", error="Missing Password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", error="User missing or bad password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
        

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        
        # Check if username field is blank
        if not request.form.get("username"):
            return render_template("error.html", error="Missing Username")
            
        # Check if password field is blank
        if not request.form.get("password"):
            return render_template("error.html", error="Missing Password")
            
        # check if confirmation of password field is blank
        if not request.form.get("confirmation"):
            return render_template("error.html", error="Password confirmation missing")
            
        # check to make sure the 2 password fields match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", error="Passwords do not match")
        
        # check if username is already being used
        test = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if test:
            return render_template("error.html", error="Username already in use")
        
        # passes all tests, regerister user into database
        db.execute("INSERT INTO users(username,hash) VALUES( ?, ?)",
                   request.form.get("username"),
                   generate_password_hash(request.form.get("password")))
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # return to main page
        return redirect("/")
        
    else:
        return render_template("register.html")


@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    """Register expenses to account"""
    
    if request.method == "POST":
        
        # check if user added a name to the expense
        if not request.form.get("name") and not request.form.get("rname"):
            return render_template("error.html", error="Must give the expense a name.")
        
        # if true then add to expenses
        if request.form.get("name"):
            
            # check if user added an amount to the expense
            if not request.form.get("amount"):
                return render_template("error.html", error="Missing amount for the expense.")
            
            # check if user has chosen a frequency for this expense 
            if not request.form.get("freq"):
                return render_template("error.html", error="Please choose a frequency for this expense.")
            
            # check if amount is a valid number
            test = request.form.get("amount").isdecimal()
            if not test:
                return render_template("error.html", error="Expense amount can only be numbers.")
            
            # check database for expense by this user with the same name
            test = db.execute("SELECT * FROM expenses WHERE user_id = ? AND name = ?",
                              int(session.get("user_id")),
                              request.form.get("name"))
            
            # if found then do not add to account
            if len(test) > 0:
                return render_template("error.html", error="Expense by that name already exists.")
            
            # insert expense into the database
            db.execute("INSERT INTO expenses (user_id, name, amount, frequency) VALUES (?, ?, ?, ?)",
                       int(session.get("user_id")),
                       request.form.get("name"),
                       float(request.form.get("amount")),
                       request.form.get("freq"))
                       
        # if false then remove expense
        else:
            
            # remove chosen expense from the database
            db.execute("DELETE FROM expenses WHERE user_id = ? AND name = ?",
                       session.get("user_id"),
                       request.form.get("rname"))
        
    # query the database for all expenses saves to users account
    expenseItems = db.execute("SELECT * FROM expenses WHERE user_id = ?", session.get("user_id"))
    
    # load page passing in the expenses to template
    return render_template("expenses.html", expenseItems=expenseItems)


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """Register income to account"""
    
    if request.method == "POST":
        
        # check if user added a name to the income
        if not request.form.get("name") and not request.form.get("rname"):
            return render_template("error.html", error="Must give the income a name.")
        
        # if true then add to income
        if request.form.get("name"):
            
            # check if user added an amount to the income
            if not request.form.get("amount"):
                return render_template("error.html", error="Missing amount for the income.")
            
            # check if user has chosen a frequency for this income
            if not request.form.get("freq"):
                return render_template("error.html", error="Please choose a frequency for this income.")
            
            # check if amount is a valid number
            test = request.form.get("amount").isdecimal()
            if not test:
                return render_template("error.html", error="Income amount can only be numbers.")
            
            # check database for expense by this user with the same name
            test = db.execute("SELECT * FROM income WHERE user_id = ? AND name = ?",
                              int(session.get("user_id")),
                              request.form.get("name"))
            
            # if found then do not add to account
            if len(test) > 0:
                return render_template("error.html", error="Income by that name already exists.")
            
            # insert income into the database
            db.execute("INSERT INTO income (user_id, name, amount, frequency) VALUES (?, ?, ?, ?)",
                       int(session.get("user_id")),
                       request.form.get("name"),
                       float(request.form.get("amount")),
                       request.form.get("freq"))
                       
        # if false then remove income
        else:
            
            # remove chosen income from the database
            db.execute("DELETE FROM income WHERE user_id = ? AND name = ?",
                       session.get("user_id"),
                       request.form.get("rname"))
        
    # query the database for all income saves to users account
    incomeItems = db.execute("SELECT * FROM income WHERE user_id = ?", session.get("user_id"))
    
    # load page passing in the expenses to template
    return render_template("income.html", incomeItems=incomeItems)


@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    """Display transactions from account"""
    
    if request.method == "POST":
        
        # check if a payment or income is chosen
        if not request.form.get("iname") and not request.form.get("pname"):
            return render_template("error.html", error="Must select an expense or income")
        
        # if a payment was selected
        if request.form.get("pname"):
            
            # check to see if an amount is selected
            if not request.form.get("pamount"):
                return render_template("error.html", error="Payment amount missing.")
            
            # insert a new transaction
            dt = datetime.datetime.today()
            db.execute("INSERT INTO transactions (user_id, name, type, amount, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?);",
                       session.get("user_id"),
                       request.form.get("pname"),
                       "Payment",
                       request.form.get("pamount"),
                       dt.day,
                       dt.month,
                       dt.year)
            
            # add new transaction ID to the expense
            currentTrans = db.execute("SELECT MAX(trans_id) FROM transactions WHERE user_id = ?;", session.get("user_id"))
            db.execute("UPDATE expenses SET last= ? WHERE user_id = ? AND name = ?",
                       currentTrans[0]["MAX(trans_id)"],
                       session.get("user_id"),
                       request.form.get("pname"))
            
            
        # if an income was selected
        else:
            
            # check to see if an amount is selected
            if not request.form.get("iamount"):
                return render_template("error.html", error="Income amount missing.")
            
            # insert a new transaction
            dt = datetime.datetime.today()
            db.execute("INSERT INTO transactions (user_id, name, type, amount, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?);",
                       session.get("user_id"),
                       request.form.get("iname"),
                       "Income",
                       request.form.get("iamount"),
                       dt.day,
                       dt.month,
                       dt.year)
            
            # add new transaction ID to the income
            currentTrans = db.execute("SELECT MAX(trans_id) FROM transactions WHERE user_id = ?;", session.get("user_id"))
            db.execute("UPDATE income SET last= ? WHERE user_id = ? AND name = ?",
                       currentTrans[0]["MAX(trans_id)"],
                       session.get("user_id"),
                       request.form.get("iname"))
            
        
    # query the database for all incomes saved to users account
    incomeItems = db.execute("SELECT * FROM income WHERE user_id = ?", session.get("user_id"))
    
    # query the database for all expenses saved to users account
    expenseItems = db.execute("SELECT * FROM expenses WHERE user_id = ?", session.get("user_id"))
    
    # query the database for all transactions saved to users account
    transItems = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY trans_id DESC", session.get("user_id"))

    # load page passing in the expenses to template
    return render_template("transactions.html", expenseItems=expenseItems, incomeItems=incomeItems, transItems=transItems)