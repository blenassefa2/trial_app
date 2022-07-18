import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")



@app.route("/" , methods=["GET", "POST"])
@login_required

def index():
    """Show public avaliable stories"""
    if request.method == "GET":

       #Select the available stories
       table= db.execute("SELECT * FROM stories ORDER BY popularity DESC")

       #Return the table to the index.html
       return render_template("index.html", table=table)

    else:

        #Get the id of the story
        story_id= request.form.get("button")

        #Using the id find the story from the tables
        story_id= db.execute("SELECT * FROM stories WHERE stories.id=:story_id ", story_id=story_id)

        #If the story is not found flash message
        if not story_id:
            flash('No story was found')
            return redirect("/")

        #If the story is found go to play page with the first row of the table with that specific id
        return render_template("play.html", title=story_id[0])



@app.route("/search", methods=["GET", "POST"])
@login_required

def search():
    """Search for a story"""

     # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("search.html")

     # User reached route via POST
    else:

        #Get the title of the story to search from user
        title=request.form.get("title")

        #Search the title from the tables
        table= db.execute("SELECT * FROM stories WHERE stories.title=:title ", title=title)
        if not table:
            table= db.execute("SELECT * FROM history WHERE title=:title AND person_id=:person_id AND played='created'", title=title,person_id=session['user_id'])
            if not table:
                #If the story is not found flash message
                flash('No story was found')
                return redirect("/search")


        #If the story is found go to play page with the first row of the table with that specific id
        return render_template("index.html", table=table)

@app.route("/create", methods=["GET", "POST"])
@login_required

def create():
    """Create a story"""

     # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("create.html")
    else:

        # Store inputs in variables to use later
        title=request.form.get("title")
        theme=request.form.get("theme")
        story=request.form.get("story")
        time = datetime.datetime.now()

        # Create a variable that will store the key words
        wo= ""

        # Create variables that will store the key word start indicator
        val="["
        n=0
        numofwords=0

        # If no key word flash message
        if not val in story:
                flash('You must include key word(s)')
                return redirect("/create")


        else:
            # Iterate through the whole story
            for t in story:

                # If key word start indicator is found copy the key word into the empy variable created to store key words (wo)
                if t=="[":
                    wo=wo+t
                    n=1
                    numofwords = numofwords + 1

                else:
                    if n!=0:
                        wo=wo+t
                        if t=="]":
                            n=0

            #If story was to be saved as public save it in both tables (history & stories) else if private save only in history
            if request.form.get("button")=="public":
                db.execute("INSERT INTO stories (story,title,numofwords,theme,keys) VALUES(:story,:title,:numofwords,:theme,:keys)",
                story=story,title=title,theme=theme,numofwords=numofwords,keys=wo)

                db.execute("INSERT INTO history (person_id,title,time,numofwords,theme,story,status,played,keys) VALUES(:person_id,:title,:time,:numofwords,:theme,:story,:status,:played,:keys)",
                person_id=session["user_id"],status="public", title=title,theme=theme,numofwords=numofwords,story=story,time=time, played="created",keys=wo)
                return redirect("/")

            else:
                db.execute("INSERT INTO history (person_id,title,numofwords,theme,time,story,status,played,keys) VALUES(:person_id,:title,:numofwords,:theme,:time,:story,:status,:played,:keys)",
                person_id=session["user_id"],status="private",played="created", title=title,story=story,theme=theme,time=time,numofwords=numofwords,keys=wo)

                return redirect("/")


@app.route("/history", methods=["GET", "POST"])
@login_required

def history():
    """Show history """

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":

       #Select the all history of current user
       table= db.execute("SELECT * FROM history WHERE person_id=:person_id ORDER BY time DESC",person_id=session["user_id"])

       #Return the table to history page
       return render_template("history.html", table=table)

    else:
        # If the user wants to delete history then delete all history of current user then flash success message
        if request.form.get("button")=="delete":
            db.execute("DELETE FROM history WHERE person_id=:id ", id=session["user_id"])
            flash('History cleared')
            return redirect("/history")

        # If user wants to play a story from their history get the id of that story
        title= request.form.get("button")
        title= db.execute("SELECT * FROM history WHERE id=:id", id=title)

        #Go to play page with the first row of the table with that specific id
        return render_template("play.html", title=title[0])


@app.route("/play", methods=["GET", "POST"])
@login_required


def play():
    """let the user play"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
       return render_template("play.html")
    else:

        # Store values in variables to use later
        time = datetime.datetime.now()

        idt= request.form.get("button")
        id_= db.execute("SELECT * FROM stories WHERE id=:id", id=idt)


        #Update values of the table
        if id_:
            p=int(id_[0]["popularity"])

            db.execute("UPDATE stories SET popularity=:popularity WHERE id=:id", popularity=p + 1, id=idt)
            db.execute("INSERT INTO history (person_id,title,time,numofwords,theme,story,status,played,keys) VALUES(:person_id,:title,:time,:numofwords,:theme,:story,:status,:played,:keys)",
            person_id=session["user_id"],status="public", title=id_[0]["title"],theme=id_[0]["theme"],numofwords=id_[0]["numofwords"],story=id_[0]["story"],time=time, played="played",keys=id_[0]["keys"])
            return redirect("/history")
        else:
            id_= db.execute("SELECT * FROM history WHERE id=:id", id=idt)

            db.execute("INSERT INTO history (person_id,title,time,numofwords,theme,story,status,played,keys) VALUES(:person_id,:title,:time,:numofwords,:theme,:story,:status,:played,:keys)",
            person_id=session["user_id"],status="public", title=id_[0]["title"],theme=id_[0]["theme"],numofwords=id_[0]["numofwords"],story=id_[0]["story"],time=time, played="played",keys=id_[0]["keys"])
            return redirect("/history")





@app.route("/about")
def about():
    """Show About us page"""

    return render_template("about.html")

@app.route("/help")
def helpe():
    """Show help page"""

    return render_template("help.html")

@app.route("/contactus")
def contact():
    """Show contact us page"""

    return render_template("contactus.html")

@app.route("/delete")
@login_required
def delete():
    """Delete the user"""
    db.execute("DELETE FROM history WHERE person_id=:id ", id=session["user_id"])
    db.execute("DELETE FROM users WHERE id=:id ", id=session["user_id"])

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Edit the user profile"""
    if request.method == "GET":
        return render_template("edit.html")
    else:
        if request.form.get("button")=="cancel":
            return redirect("/")
         # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
         # Ensure password was submitted
        elif not request.form.get("re-password"):
            return apology("must re-enter password", 403)
        elif not request.form.get("username"):
            return apology("must provide username", 403)
        else:

             # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))
            if len(rows) == 1:
                return apology("username is already used", 403)
            elif request.form.get("password") != request.form.get("re-password"):
                return apology("you must re-enter same password", 403)
            else:
                username = request.form.get("username")
                pas = request.form.get("password")
                password =  generate_password_hash(pas)

                db.execute("UPDATE users SET username=:username,hash=:password WHERE id=:id", username=username, password=password, id=session["user_id"])
                # Remember which user has logged in

                flash('Edited!')
                return redirect("/")




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



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")
    else:

         # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) == 1:
            return apology("username is already used", 403)
        elif request.form.get("password") != request.form.get("re-password"):
            return apology("you must re-enter same password", 403)
        else:
            username = request.form.get("username")
            pas = request.form.get("password")
            password =  generate_password_hash(pas)

            db.execute("INSERT INTO users (username,hash) VALUES (:username, :password)", username=username, password=password)
            # Remember which user has logged in
            row = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))


            # Remember which user has logged in
            session["user_id"] = row[0]["id"]
            flash('Registered!')
            return redirect("/")





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
