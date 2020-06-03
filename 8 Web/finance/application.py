import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userId = session["user_id"]
    totalWorth = 0
    # get cash for  user
    cash = db.execute("SELECT * FROM users WHERE id == :userId", userId = userId)[0]["cash"]
    totalWorth += cash

    # get all stocks owned
    ownedStocks = db.execute("SELECT stock, quantity FROM ownership WHERE userid == :userId ORDER BY stock", userId = userId)
    stockInfoList = []

    # Create a custom dict of stock details
    for stock in ownedStocks:
        stockInfo = {}
        stockDetails = lookup(stock['stock'])

        stockInfo["symbol"] = stock["stock"]
        stockInfo["quantity"] = stock["quantity"]
        stockInfo["name"] = stockDetails['name']
        stockInfo["price"] = usd(stockDetails['price'])

        stockWorth = stockDetails['price'] * stock["quantity"]
        totalWorth += stockWorth

        stockInfo["total"] = usd(stockWorth)

        stockInfoList.append(stockInfo)

    return render_template("index.html", totalWorth = usd(totalWorth), cash = usd(cash), stocks = stockInfoList)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # getting and checking form values
        symbolInput = request.form.get("symbol")
        if symbolInput == '':
            return apology("No symbol entered", 400)
        symbol = lookup(symbolInput)
        if symbol == None:
            return apology("invalid symbol", 400)

        quantityInput = request.form.get("shares")
        if quantityInput == '':
            return apology("Quantity not selected", 400)

        try:
            quantity = int(quantityInput)
        except:
            return apology("Invalid shares", 400)

        if quantity < 1:
            return apology("invalid number", 400)

        price = symbol["price"]
        symbolCode = symbol["symbol"]
        userId = session["user_id"]

        orderTotal = price * quantity
        userFunds = db.execute("SELECT cash FROM users WHERE id == :userId", userId = userId)
        newBalance = userFunds[0]['cash'] - orderTotal

        if newBalance < 0:
            return apology("can't afford", 400)
        else:
            db.execute("UPDATE users SET cash = :newBalance WHERE id = :userId", newBalance = newBalance, userId = userId)

        dt = datetime.now()
        # make record of transaction
        db.execute("INSERT INTO history (userid, datetime, stock, quantity, priceEach) VALUES (:userid, :datetime, :stock, :quantity, :price)",
                    userid = userId, datetime = dt, stock = symbolCode, quantity = quantity, price = price)

        # update or insert ownership of stock
        existingOwnership = db.execute("SELECT entryid FROM ownership WHERE userid == :userId AND stock == :symbol", userId = userId, symbol = symbolCode)
        if len(existingOwnership) != 1:
            db.execute("INSERT INTO ownership (userid, stock, quantity) VALUES (:userid, :stock, :quantity)", userid = userId, stock = symbolCode, quantity = quantity)
        else:
            currentQuantity = db.execute("SELECT quantity FROM ownership WHERE entryid == :entryid", entryid = existingOwnership[0]['entryid'])
            newQuantity = currentQuantity[0]['quantity'] + quantity
            db.execute("UPDATE ownership SET quantity = :newQuantity WHERE entryid == :entryid", newQuantity = newQuantity, entryid = existingOwnership[0]['entryid'])

        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    userId = session["user_id"]
    transactions = db.execute("SELECT stock, quantity, priceEach, datetime FROM history WHERE userid = :userId", userId = userId)

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        resp = lookup(symbol)

        if resp != None:
            symbol = resp["symbol"]
            symbolName = resp["name"]
            symbolPrice = usd(resp["price"])
            return render_template("quoted.html", symbol=symbol, symbolName=symbolName, symbolPrice=symbolPrice)
        else:
            return apology("invalid symbol", 400)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passwordMatch =  request.form.get("passwordMatch")

        # Form validation
        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)
        elif not passwordMatch:
            return apology("must confirm password", 403)
        elif not password == passwordMatch:
            return apology("passwords must match", 400)

        # register user if username not taken
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) == 1:
            return apology("username taken", 403)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=generate_password_hash(password))

        # get the entry of the name just added
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # set session (log in) and redirect
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    userId = session["user_id"]

    if request.method == "POST":
        # Get and check values from form
        symbol = request.form.get("symbol")
        if symbol == None:
            return apology("Symbol not selected", 400)
        sharesInput = request.form.get("shares")
        if sharesInput == '':
            return apology("Quantity not selected", 400)
        try:
            shares = int(sharesInput)
        except:
            return apology("Invalid shares", 400)


        symbolQuantity = db.execute("SELECT quantity FROM ownership WHERE userid = :userId AND stock = :stock", userId = userId, stock = symbol)[0]["quantity"]

        # Check it is a valid request
        if symbolQuantity < 1:
            return apology("Share not owned", 400)
        if shares < 1:
            return apology("invalid number", 400)
        if shares > symbolQuantity:
            return apology("Too many shares", 400)

        # Update cash balance
        symbolInfo = lookup(symbol)
        saleTotal = symbolInfo["price"] * shares
        currentUserBalance = db.execute("SELECT cash FROM users WHERE id = :userId", userId = userId)
        newBalance= saleTotal + currentUserBalance[0]["cash"]
        db.execute("UPDATE users SET cash = :newBalance WHERE id = :userId", newBalance = newBalance, userId = userId)

        # write to history
        dt = datetime.now()
        db.execute("INSERT INTO history (userid, datetime, stock, quantity, priceEach) VALUES (:userid, :datetime, :stock, :quantity, :price)",
                    userid = userId, datetime = dt, stock = symbol, quantity = (shares - (shares * 2)), price = symbolInfo["price"])

        # remove from owned stocks
        if shares == symbolQuantity:
            db.execute("DELETE FROM ownership WHERE userid = :userId AND stock = :symbol", userId = userId, symbol = symbol)
        else:
            newQuantity = symbolQuantity - shares
            db.execute("UPDATE ownership SET quantity = :newQuantity WHERE userid = :userId AND stock = :symbol",
                        newQuantity = newQuantity, userId = userId, symbol = symbol)

        return redirect("/")

    else:
        stocks = db.execute("SELECT stock FROM ownership WHERE userid = :userId ORDER BY stock", userId = userId)
        return render_template("sell.html", stocks = stocks)


@app.route("/panicsell", methods=["POST"])
@login_required
def panicsell():
    """Panic sell all shares of stock"""
    userId = session["user_id"]

    # Keep running count of cash after each sale
    currentCashTotal = db.execute("SELECT cash FROM users WHERE id = :userId", userId = userId)[0]['cash']
    stocksHeld = db.execute("SELECT stock, quantity FROM ownership WHERE userid = :userId", userId = userId)
    if len(stocksHeld) < 1:
        return apology("No shares owned", 400)

    for stock in stocksHeld:
        stockInfo = lookup(stock["stock"])
        stockPrice = stockInfo["price"]
        stockQuantity = stock["quantity"]
        currentCashTotal += (stockPrice * stockQuantity)
        dt = datetime.now()

        # Make transaction entry
        db.execute("INSERT INTO history (userid, datetime, stock, quantity, priceEach) VALUES (:userid, :datetime, :stock, :quantity, :price)",
                    userid = userId, datetime = dt, stock = stockInfo["symbol"], quantity = (stockQuantity - (stockQuantity * 2)), price = stockPrice)

    # Remove all owned stocks
    db.execute("DELETE FROM ownership WHERE userid = :userId", userId = userId)
    # Update the cash total
    db.execute("UPDATE users SET cash = :newBalance WHERE id = :userId", newBalance = currentCashTotal, userId = userId)

    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
