'''
jazzy-ostriches
Final Project: Lost & Found
Alessandro Cartegni, Brian Leung, Dasha Shifrina, Joyce Wu
'''

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from util import auth, database
import urllib2, json
from util import mailplane

app = Flask(__name__)
app.secret_key = os.urandom(32)

#opens api key text file and retrieves keys
f = open("keys.txt", "r")
apis = f.read().split("\n")
map_api_key = apis[1]

#homepage
@app.route("/")
def start():
    found = database.find_unique_locations('found')
    lost = database.find_unique_locations('lost')
    if session.get('username'):
        #must add more once home.html has more details
        return render_template('home.html', title="Welcome", loggedIn=True, api_key=map_api_key, lost_listings=lost, found_listings=found)
    return render_template('home.html', title="Welcome", loggedIn=False, api_key=map_api_key, lost_listings=lost, found_listings=found)


#search bar fxn

@app.route("/lost_search", methods=["GET","POST"])
def lost_search():
    keyword = ''
    category = ''
    unique_locations = database.find_unique_locations('lost')
    r = request.form
    if "search" in r:
        keyword = r["search"]
   # print keyword
    if "category" in r:
        category = r["category"]
    #print category
    item_list = database.lost_filter_search(keyword, category, "lost")
        #must add more once home.html has more details
    return render_template("lost_postings.html", api_key=map_api_key, listings=item_list, unique=unique_locations)

@app.route("/found_search", methods=["GET","POST"])
def found_search():
    keyword = ''
    category = ''
    unique_locations = database.find_unique_locations('found')
    r = request.form
    if "search" in r:
        keyword = r["search"]
    #print keyword
    if "category" in r:
        category = r["category"]
   # print category
    item_list = database.lost_filter_search(keyword, category, "found")
        #must add more once home.html has more details
    return render_template("found_postings.html", api_key=map_api_key, listings=item_list, unique=unique_locations)

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
        lost = database.user_items(username, 'lost')
        found = database.user_items(username, 'found')
        print(lost)
        return render_template("profile.html", loggedIn = True, lost_items=lost, found_items=found, user=username)

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

#route for reporting an item user found
@app.route('/found', methods=['GET', 'POST'])
def post():
    if not session.get('username'):
        flash("Yikes! You need to log in first.")
        return redirect(url_for('authentication'))
    else:
        return render_template('create_posting.html', loggedIn=True)

#route for creating listing for found item

@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('username'):
        flash("Yikes! You need to log in first.")
        return redirect(url_for('authentication'))
    username = session.get('username')
    r = request.form
    if "item" in r and "category" in r and "location" in r and "date" in r and "description" in r:
        database.add_found_item(username, r["item"],r["category"], r["date"], r["location"], r["description"])
        possible_matches = database.find_found_match(r["item"], r["category"], r["location"], r["description"])
        return render_template("maybe_postings.html", loggedIn=True, matches = possible_matches, found=True, lost_found="found")
    else:
        flash("Your item was not reported properly. Please try again.")
        return redirect(url_for('post'))

#route for creating listing for lost item
@app.route('/find_item', methods=['GET', 'POST'])
def find():
    if not session.get('username'):
        flash("Yikes! You need to log in first.")
        return redirect(url_for('authentication'))
    username = session.get('username')
    r = request.form
    if "item" in r and "category" in r and "location" in r and "date" in r and "description" in r:
        database.add_lost_item(username, r["item"],r["category"], r["date"], r["location"], r["description"])
        possible_matches = database.find_lost_match(r["item"], r["category"], r["location"], r["description"])
        return render_template("maybe_postings.html", loggedIn=True, matches = possible_matches, found=False, lost_found="lost")
        flash("Your item was not reported properly. Please try again.")
        return redirect(url_for('list_lost_items'))

@app.route('/lost_postings', methods=['GET', 'POST'])
def list_lost_items():
    list = database.item_listings('lost')
    unique_locations = database.find_unique_locations('lost')
    #you are still allowed to see postings without logging in
    if not session.get('username'):
        return render_template("lost_postings.html", loggedIn=False, api_key=map_api_key, listings=list, unique=unique_locations)
    else:
        return render_template("lost_postings.html", loggedIn=True, api_key=map_api_key, listings=list, unique=unique_locations)

@app.route('/found_postings', methods=['GET', 'POST'])
def list_found_items():
    list = database.item_listings('found')
    unique_locations = database.find_unique_locations('found')
    #still allowed to see postings without logging in
    if not session.get('username'):
        return render_template("found_postings.html", loggedIn=False, api_key=map_api_key, listings=list, unique=unique_locations)
    else:
        return render_template("found_postings.html", loggedIn=True, api_key=map_api_key, listings=list, unique=unique_locations)

@app.route('/single_posting', methods=['GET', 'POST'])
def single_post():
    item = database.get_item(request.form.get('item_id'), request.form.get('lost_found'))
    if not session.get('username'):
        return render_template("single_posting.html", loggedIn=False, item=item)
    else:
        print(item)
        return render_template("single_posting.html", loggedIn=True, item=item)

@app.route('/send', methods = ['GET','POST'])
def send():
    if not session.get('username'):
        flash('Looks like you need to login!')
        return redirect(url_for('authentication'))
    else:
        userID = int(mailplane.getUserID(session.get('username')))
        itemID = int(request.args.get('item_id'))
        mailplane.sendMail(userID,itemID,0)
        return redirect('/sent')

@app.route('/sent', methods = ['GET','POST'])
def sent():
    if not session.get('username'):
        flash('Looks like you need to login!')
        return redirect(url_for('authentication'))
    else:
        return render_template("sent.html", loggedIn=True)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if not session.get('username'):
        flash('Looks like you need to login!')
        return redirect(url_for('authentication'))
    else:
        if request.form.get('delete') == "Delete":
            item = int(request.form.get('id'))
            lost_found = request.form.get('lost_found')
            print item
            print lost_found
            schema = ["item_id","item","description","category","location","date"]
            lostness = 1
            if lost_found == 'lost':
                lostness = 0
            auth.delete_item(lostness,item)
            return redirect(url_for('profile'))
        else:
            item = request.form.get('id')
            lost_found = request.form.get('lost_found')
            print lost_found
            print "HAPPENING"
            listing = database.get_item(item, lost_found)
            print listing
            print "HAPPENED"
            return render_template("edit_post.html", item=listing, lostOrFound=lost_found, loggedIn=True)

@app.route('/editor', methods=["GET","POST"])
def editor():
    if not session.get('username'):
        flash('Looks like you need to login!')
        return redirect(url_for('authentication'))
    else:
        schema = ["item_id","item","description","category","location","date"]
        lostness = 1
        if request.args.get("lostOrFoundVal") == 'lost':
            lostness = 0
            print "ITS LOST!"
        print("itemid: "+request.args.get("item_id"))
        itemid = int(request.args.get("item_id"))
        i = 1
        dataIndices = [1,2,3,5,8]
        print "lostness is: "+str(lostness)
        print "itemid is: "+str(itemid)
        for dataIndex in dataIndices:
            print i
            print "lostness: "+str(lostness)
            newVal = str(request.args.get(schema[i]))
            auth.edit_item(newVal,lostness,itemid,dataIndex)
            i+=1
        return redirect(url_for('edited'))

@app.route('/edited',methods=["GET","POST"])
def edited():
    if not session.get('username'):
        flash('Looks like you need to login!')
        return redirect(url_for('authentication'))
    else:
        return render_template("edited.html", loggedIn=True)
'''
@app.route('/deletion',methods=["GET","POST"])
def deletion():
    '''

if __name__ == "__main__":
    app.debug = True
    app.run()
