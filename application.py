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
    return render_template("index.html")


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
        return TODO
    else:
        return render_template("expenses.html")


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """Register income to account"""
    
    if request.method == "POST":
        return TODO
    else:
        return render_template("income.html")


@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    """Display transactions from account"""
    
    if request.method == "POST":
        return TODO
    else:
        return render_template("transactions.html")