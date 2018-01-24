import sqlite3
import random
import os
import urllib2
import json

#opens api key text file and retrieves keys
f = open("keys.txt", "r")
apis = f.read().split("\n")
map_api_key = apis[1]
#dasha tasks:
  #
# only has login functionality so far

#fxns available: getting users, adding users, getting user's lost items, adding lost item to user account, item listing

#opens api key text file and retrieves keys
#f = open("keys.txt", "r")
#apis = f.read().split("\n")
#map_api_key = apis[1]

# -----FUNCTIONS FOR LOGIN SYSTEM-----
# returns a dictionary for user data {user: pass}
def getUsers():
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT username, pass FROM users'
    x = c.execute(a)
    users = {}
    for line in x:
        users[line[0]] = line[1]
    db.close()
    return users


# add the login to the database
def addUser(user, password, email):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    vals = [user, password, email]
    c.execute("INSERT INTO users (username, pass, email) VALUES(?, ?, ?)", vals)
    db.commit()
    db.close()


# ----- FUNCTIONS FOR LATITUDE AND LONGITUDE

def get_latitude(location):
    loc = location.replace(" ", "+")
    uResp = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '&key=' + map_api_key)
    blah = uResp.read()
    #print blah
    dict1 = json.loads(blah)
    return dict1["results"][0]["geometry"]["location"]["lat"]


def get_longitude(location):
    loc = location.replace(" ", "+")
    uResp = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '&key=' + map_api_key)
    blah = uResp.read()
    #print blah
    dict1 = json.loads(blah)
    return dict1["results"][0]["geometry"]["location"]["lng"]


# -----FUNCTIONS FOR ITEM SYSTEM-----

##helper fxn for last id

def last_lost_id():
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    num_row = "SELECT Count(*) FROM lost_items"
    y = c.execute(num_row)
    for bar in y:
        if bar[0] == 0:
            return 0
    last_id = 'SELECT * FROM lost_items WHERE id=(SELECT max(id) FROM lost_items)'
    x = c.execute(last_id)
    for bar in x:
        return bar[0]

def last_found_id():
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    num_row = "SELECT Count(*) FROM found_items"
    y = c.execute(num_row)
    for bar in y:
        if bar[0] == 0:
            return 0
    last_id = 'SELECT * FROM found_items WHERE id=(SELECT max(id) FROM found_items)'
    x = c.execute(last_id)
    for bar in x:
        return bar[0]

#print last_found_id()

#possible item match list for lost item
def find_lost_match(lost_item, category, location, description):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT * from found_items'
    x = c.execute(a)
    possible_matches = []
    for bar in x:
        similarity = 0
        if(lost_item == bar[1]):
            similarity += 2
        if(description == bar[2]):
            similarity += 20
        if(category == bar[3]):
            similarity += 1
        if(location == bar[5]):
            similarity += 2
        if similarity > 0:
            item = {}
            item['item_id'] = bar[0]
            item['item_name'] = bar[1]
            item['item_desc'] = bar[2]
            item['item_cat'] = bar[3]
            item['item_acc_id'] = bar[4]
            item['item_location'] = bar[5]
            item['item_lat'] = bar[6]
            item['item_long'] = bar[7]
            item['bar_date'] = bar[8]
            item['similarity'] = similarity
            possible_matches.append(item)
            return possible_matches
    db.commit()
    db.close()

#possible item match list for found item
def find_found_match(found_item, category, location, description):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT * from lost_items'
    x = c.execute(a)
    possible_matches = []
    for bar in x:
        similarity = 0
        if(found_item == bar[1]):
            similarity += 2
        if(description == bar[2]):
            similarity += 20
        if(category == bar[3]):
            similarity += 1
        if(location == bar[5]):
            similarity += 2
        if similarity > 0:
            item = {}
            item['item_id'] = bar[0]
            item['item_name'] = bar[1]
            item['item_desc'] = bar[2]
            item['item_cat'] = bar[3]
            item['item_acc_id'] = bar[4]
            item['item_location'] = bar[5]
            item['item_lat'] = bar[6]
            item['item_long'] = bar[7]
            item['bar_date'] = bar[8]
            item['similarity'] = similarity
            possible_matches.append(item)
            return possible_matches
    db.commit()
    db.close()

#add lost item to database
def add_lost_item(user, item, category, date, location, description):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    item_id = last_lost_id() + 1
    lost_items_vals = [item_id, item, description, category, user, location, get_latitude(location + " NY"), get_longitude(location + " NY"), date]
    c.execute("INSERT INTO lost_items (id, item, description, category, account_id, location, lat, long, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", lost_items_vals)
    ##appending lost item
    a = 'SELECT username, l_lost FROM users'
    x = c.execute(a)
    for bar in x:
        if(user == bar[0]):
            if bar[1] is None:
                wow = str(item_id)
            else:
                wow = bar[1]
                wow+= "," + str(item_id)
          #  if wow == "":
          #      wow = str(item_id)
          #  else:

            c.execute("UPDATE users SET l_lost='" + wow + "' WHERE username = '" + user + "'")
    db.commit()
    db.close()

#add found item to database
def add_found_item(user, item, category, date, location, description):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    item_id = last_found_id() + 1
    found_items_vals = [item_id, item, description, category, user, location, get_latitude(location+" NY"), get_longitude(location + " NY"), date]
    c.execute("INSERT INTO found_items (id, item, description, category, account_id, location, lat, long, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", found_items_vals)
    ##appending lost item
    a = 'SELECT username, l_found FROM users'
    x = c.execute(a)
    for bar in x:
        if(user == bar[0]):
            if bar[1] is None:
                wow = str(item_id)
            else:
                wow = bar[1]
           # if not isinstance(wow, str):
              #  wow = str(item_id)
                wow += "," + str(item_id)
            c.execute("UPDATE users SET l_found='" + wow + "' WHERE username = '" + user + "'")
    db.commit()
    db.close()

#add_found_item("joyce", "house", "accessory", "06/08/2018", "Times Square", "I couldn't find the owner so I broke in. Lmk if its yours. Yellow with a wooden awning. 3 bedroom.")

def item_listings(lost_found):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT * FROM ' + lost_found + '_items'
    x = c.execute(a)
    item_list = []
    for bar in x:
        item_id = bar[0]
        item_name = bar[1]
        item_desc = bar[2]
        item_cat = bar[3]
        item_lat = bar[6]
        item_long = bar[7]
        item_location = bar[5]
        item_date = bar[8]
        ##add vars for location string and date
        item = {}
        item['item_id'] = item_id
        item['item_cat'] = item_cat
        item['item_name'] = item_name
        item['item_desc'] = item_desc
        item['item_lat'] = item_lat
        item['item_long'] = item_long
        item['item_location'] = item_location
        item['item_date'] = item_date
        item_list.append(item)
        ##add rows for location string and date
    db.commit()
    db.close()
    return item_list

def lost_filter_search(keyword,category, lost_found):
    lost_items = item_listings(lost_found)
    result = []
    #print lost_items
    if keyword != "":
        for things in lost_items:
            if (keyword in things["item_name"]):
                result.append(things)
    if category != "none" and keyword == "":
        for things in lost_items:
            if(category in things["item_cat"]):
                result.append(things)
    if category != "none" and keyword != "":
        result2 = []
        for things in result:
            if(category in things["item_cat"]):
                result2.append(things)
        result = result2
    ###write date sorting part
    return result

#print lost_filter_search("ca","")

def find_unique_locations(lost_found):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT lat, long FROM ' + lost_found + '_items'
    x = c.execute(a)
    locations = []
    for loc in x:
        if (loc not in locations):
            locations.append(loc)
    return locations

def get_item(id, lost_found):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT * FROM ' + lost_found + '_items WHERE id=' + str(id)
    x = c.execute(a)
    item = []
    for y in x:
        for info in y:
            item.append(info)
    #print(item)
    return item

#get_item(0, "lost")

#print all lost items from user
def user_items(user, lost_found):
    if lost_found == 'lost':
        l_f = 'l_lost'
    else:
        l_f = 'l_found'
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT username, ' + l_f + ' FROM users'
    x = c.execute(a)
    items = []
    #gets list of postings from users table, then retrieves item info from lost/found database
    for bar in x:
        if(user == bar[0]):
            list_of_postings = bar[1]
            if(list_of_postings is None):
                posts = []
            else:
                posts = list_of_postings.split(",")
   # print posts
    for post in posts:
        if(post != ''):
            items.append(get_item(int(post), lost_found))
    db.commit()
    db.close()
    return items

#print user_items("dashak", "found")

'''
# execute this file to create the initial database
if __name__ == '__main__':
    # initialize database
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    # table for user login
    c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, pass TEXT, l_found TEXT, l_lost TEXT);")
    #table with postings for lost items
    c.execute("CREATE TABLE lost_items (id INT, item TEXT, description TEXT, category TEXT, account_id INT, lat FLOAT, long FLOAT);")
    #table with postings for found items
    c.execute("CREATE TABLE found_items (id INT, item TEXT, description TEXT, category TEXT, account_id INT, lat FLOAT, long FLOAT);")
    db.commit()
    db.close()'''
