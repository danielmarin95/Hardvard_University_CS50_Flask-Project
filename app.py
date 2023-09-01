import re
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show list of book reviews"""
    # Getting the list of reivews by the logged on user
    books = db.execute("SELECT * FROM book_reviews WHERE user_id = ? ORDER BY title COLLATE NOCASE ASC;", session["user_id"])
    # Getting the number of reviews, to show on the title
    books_count = db.execute("SELECT COUNT(title) FROM book_reviews WHERE user_id = ?;", session["user_id"])

    return render_template("index.html", books=books, books_count=books_count[0]['COUNT(title)'])

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Confirming information is correctly posted
        if not (username := request.form.get("username")):
            return apology("Username is missing")

        if not (password := request.form.get("password")):
            return apology("Password is missing")

        if not (confirmation := request.form.get("confirmation")):
            return apology("Confirmation passowrd does not match")

        # Verifying password security
        if (len(password) < 8):
            return apology("The password must contain at least 8 characters")
        SPECIAL_CHARACTERS = ['-', '_', '?', '!', '$', '%', '(', ')', '{', '}', '*', '.', ',']
        character_present = False
        for character in SPECIAL_CHARACTERS:
            if (character in password):
                character_present = True
        if not (character_present):
            return apology("The password must contain at least one special character")
        if not (re.search('[a-zA-Z]', password)):
            return apology("The password must contain at least one letter")
        if not (re.search('[0-9]', password)):
            return apology("The password must contain at least one number")

        # Confirms if the user name exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # In case the username is not in the database
        if len(rows) != 0:
            return apology(f"The username '{username}' already exists. Please choose another name.")

        # Checking the passwords are matching
        if password != confirmation:
            return apology("Password does not match")

        # Inserting the username in the database
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                        username, generate_password_hash(password))

        # Remembers the logged-in user
        session["user_id"] = id

        flash("You have been registered successfully!")

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/create-review", methods=["GET", "POST"])
@login_required
def review_creator():
    """Show form to submit review"""

    # Confirming all information is present
    if request.method == "POST":
        if not (title := request.form.get("title")):
            return apology("Title is missing")
        if not (author := request.form.get("author")):
            return apology("Author is missing")
        if not (points := request.form.get("points")):
            return apology("Points are missing")
        if not (review := request.form.get("review")):
            return apology("Review is missing")

        # Running the query to insert the book review
        db.execute("INSERT INTO book_reviews (title, author, points, review, user_id) VALUES (?, ?, ?, ?, ?);",
            title, author, points, review, session["user_id"])

        flash("Review added successfully")
        return redirect("/")

    else:
        return render_template("create-review.html")

@app.route("/edit-review", methods=["GET", "POST"])
@login_required
def review_editor():
    """Show prefilled form to edit review"""
    if request.method == "POST":

        # Confirming all information is present
        if not (book_id := request.form.get("book_id")):
            return apology("Id is missing. Stop Hacking!")
        if not (title := request.form.get("title")):
            return apology("Title is missing")
        if not (author := request.form.get("author")):
            return apology("Author is missing")
        if not (points := request.form.get("points")):
            return apology("Points are missing")
        if not (review := request.form.get("review")):
            return apology("Review is missing")

        # Inserting the review into the database, under that username
        db.execute("UPDATE book_reviews SET title = ?, author = ?, points = ?, review = ? WHERE id = ? AND user_id = ?;",
            title, author, points, review, book_id, session["user_id"])

        flash("Review edited successfully!")
        return redirect("/")

    else:

        # Confirm there was a book id on the URL
        if not (book_id := request.args.get("id")):
            return redirect("/create-review")

        # This will make sure the logged in user can only edit books under their name
        books = db.execute("SELECT * FROM book_reviews WHERE id = ? AND user_id = ?;", int(book_id), session["user_id"])

        # If there are no books with that Id for that userId it will just load an empty review
        if not (books):
            return redirect("/create-review")

        # The SQL returns an array, so we should only select the first element
        return render_template("edit-review.html", book=books[0])

@app.route("/delete-review", methods=["GET"])
@login_required
def review_deleter():
    """Show form to submit review"""
    # Confirm there was a book id on the URL
    if not (book_id := request.args.get("id")):
        return redirect("/create-review")

    #Confirming that the review entered is from the user
    reviews = db.execute("SELECT * FROM book_reviews WHERE id = ? AND user_id = ?;", int(book_id), session["user_id"])
    if len(reviews) == 0:
        flash("There is no such book review under your name!")
        return redirect("/")

    # This will make sure the logged in user can only delete books under their name
    db.execute("DELETE FROM book_reviews WHERE id = ? AND user_id = ?;", int(book_id), session["user_id"])

    flash("Review deleted successfully!")
    return redirect("/")


@app.route("/desired-books")
@login_required
def desired_books_index():
    """Show general list of desired books"""

    # Getting the list of all desired books regardless of user
    books = db.execute("SELECT * FROM desired_books ORDER BY title COLLATE NOCASE ASC;")
    desired_books_users = db.execute("SELECT * FROM desired_books_users WHERE user_id = ?", session["user_id"] )
    return render_template("desired-books.html", books=books, desired_books_users=desired_books_users, personal_list=False)

@app.route("/only-my-list")
@login_required
def user_desired_list_index():
    """Show the list of desired books of the user"""

    # Getting the list of all desired books only for this user
    books = db.execute("SELECT * FROM desired_books JOIN desired_books_users ON desired_books_users.desired_book_id = desired_books.id WHERE desired_books_users.user_id = ? ORDER BY desired_books.title COLLATE NOCASE ASC;", session["user_id"])
    desired_books_users = db.execute("SELECT * FROM desired_books_users WHERE user_id = ?", session["user_id"] )
    return render_template("desired-books.html", books=books, desired_books_users=desired_books_users, personal_list=True)

@app.route("/create-desired-book", methods=["GET", "POST"])
@login_required
def desired_books_creator():
    """Show form to add a new book to the general list"""

    # Confirming all information is present
    if request.method == "POST":
        if not (title := request.form.get("title")):
            return apology("Title is missing")
        if not (author := request.form.get("author")):
            return apology("Author is missing")

        # Checking if the book is already in the general list
        desired_books = db.execute("SELECT * FROM desired_books WHERE title = ? AND author = ?;",
            title, author)

        # In case the book is already in the desired_books table
        if len(desired_books) != 0:
            desired_books_users = db.execute("SELECT * FROM desired_books_users WHERE user_id = ? and desired_book_id = ?", session["user_id"], int(desired_books[0]['id']))
            if len(desired_books_users) != 0:
                flash("You already have this book in your personal list")
                return redirect("/desired-books")
            else:
                db.execute("INSERT INTO desired_books_users (user_id, desired_book_id) VALUES (?, ?);",
                    session["user_id"], int(desired_books[0]['id']))
                flash("Added the book to your personal list")
                return redirect("/desired-books")

        # Running the query to insert the book review
        desired_book_id = db.execute("INSERT INTO desired_books (title, author) VALUES (?, ?);",
            title, author)

        db.execute("INSERT INTO desired_books_users (user_id, desired_book_id) VALUES (?, ?);",
                    session["user_id"], desired_book_id)

        flash("New book added to your list!")
        return redirect("/desired-books")

    else:
        return render_template("create-desired-book.html")

@app.route("/add-to-list", methods=["GET"])
@login_required
def add_to_list():
    """Add the requested book to the desired list of the user"""

    # Confirm Id of the book is submitted
    if not (book_id := request.args.get("id")):
        return apology("Book Id is missing. Hacking is wrong!")

    # Confirm that the book is not already on the list of the user
    desired_books_users = db.execute("SELECT * FROM desired_books_users WHERE user_id = ? and desired_book_id = ?", session["user_id"], int(book_id))
    if len(desired_books_users) != 0:
        flash("You already have this book in your personal list. Hacking is bad!")
        return redirect("/desired-books")

    # Adding the book to the desired list of the user
    db.execute("INSERT INTO desired_books_users (user_id, desired_book_id) VALUES (?, ?);",
                    session["user_id"], book_id)

    flash("Book successfully added to your list!")
    return redirect("/desired-books")

@app.route("/remove-from-list", methods=["GET"])
@login_required
def remove_from_list():

    """Remove the requested book from the desired list of the user"""

    # Confirm Id of the book is submitted
    if not (book_id := request.args.get("id")):
        return apology("Book Id is missing. Hacking is wrong!")

    # Adding the book to the desired list of the user
    db.execute("DELETE FROM desired_books_users WHERE user_id = ? AND desired_book_id = ?;",
                    session["user_id"], int(book_id))

    flash("Book successfully removed from your list!")
    return redirect("/desired-books")

@app.errorhandler(404)
def invalid_route(e):
    return apology("404! You arrived to Patrick's dream...")