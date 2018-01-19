'''
jazzy-ostriches
Final Project: Lost & Found
Alessandro Cartegni, Brian Leung, Dasha Shifrina, Joyce Wu
'''

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from util import auth, database
import urllib2, json

app = Flask(__name__)
app.secret_key = os.urandom(32)

#opens api key text file and retrieves keys
f = open("keys.txt", "r")
apis = f.read().split("\n")
map_api_key = apis[0]

#homepage
@app.route("/")
def start():
    if session.get('username'):
        #must add more once home.html has more details
        return render_template('home.html', title="Welcome", loggedIn=True, api_key=map_api_key)
    #must add introductory page to explain what everything is
    return render_template('home.html', title="Welcome", loggedIn=False, api_key=map_api_key)

# Login Authentication
@app.route('/login', methods=['GET', 'POST'])
def authentication():
    # if user already logged in, redirect to homepage(base.html)
    if session.get('username'):
        flash("Yikes! You're already signed in.")
        return redirect(url_for('start'))
    # user entered login form
    elif request.form.get('login'):
        print "login"
        return auth.login()
    # user didn't enter form
    else:
        return render_template('login.html', title = "Login", loggedIn=False)

#Sign up for new account
@app.route('/signup', methods=['GET', 'POST'])
def crt_acct():
    if session.get('username'):
        flash("Yikes! You're already signed in.")
        return redirect(url_for('start')) #goes back to home page
    # user entered signup form
    elif request.form.get('signup'):
        return auth.signup()
    else:
        return render_template('signup.html', title = "Signup", loggedIn=False)

# Profile page - shows profile stats and (if time, allow them to change password)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('username'):
        flash("Yikes! You need to log in first.")
        return redirect(url_for('authentication'))
    else:
        username = session.get('username')
        return render_template("profile.html", loggedIn = True)

# Logging out
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not session.get('username'):
        flash("Yikes! You're not logged in")
    else:
        flash("Yay! You've successfully logged out")
        session.pop('username')
        return redirect(url_for('start')) #returns back to main page once logged out

@app.route('/lost', methods=['GET', 'POST'])
def lost_item():
    if not session.get('username'):
        flash("Yikes! You're not logged in.")
        return redirect(url_for('authentication'))
    else:
        return render_template("create_lost_post.html", loggedIn = True)

@app.route('/found', methods=['GET', 'POST'])
def post():
    if not session.get('username'):
        flash("Yikes! You need to log in first.")
        return redirect(url_for('authentication'))
    else:
        return render_template('create_posting.html') #go back and add more variables

@app.route('/find_item', methods=['GET', 'POST'])
def find():
    found = True #filler boolean for now, method that helps find item
    if found:
        return render_template("single_posting.html") #use ajax instead, if not found, give option to add posting
    else:
        flash("Sorry, we could not find a match. We will add your lost item to the listing.")
        return redirect(url_for('list_lost_items'))

@app.route('/lost_postings', methods=['GET', 'POST'])
def list_lost_items():
    list = database.item_listings()
    #you are still allowed to see postings without logging in
    if not session.get('username'):
        return render_template("lost_postings.html", loggedIn=False, api_key=map_api_key, listings=list)
    else:
        return render_template("lost_postings.html", loggedIn=True, api_key=map_api_key, listings=list)

@app.route('/found_postings', methods=['GET', 'POST'])
def list_found_items():
    #still allowed to see postings without logging in
    if not session.get('username'):
        return render_template("found_postings.html", loggedIn=False)
    else:
        return render_template("found_postings.html", loggedIn=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
