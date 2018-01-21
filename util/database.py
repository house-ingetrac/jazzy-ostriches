import sqlite3
import random


#dasha tasks:
  #
# only has login functionality so far

#fxns available: getting users, adding users, getting user's lost items, adding lost item to user account, item listing



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

# -----FUNCTIONS FOR ITEM SYSTEM-----

#print all lost items from user
def lost_items(user):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT username, l_lost FROM users'
    x = c.execute(a)
    lost_items = {}
    for bar in x:
        if(user == bar[0]):
            wow = bar[1]
            print wow
            eyo = wow.split(",")
            #INSERT LINE TO PRINT ITEMS BY NUMBER
    db.commit()
    db.close()

##helper fxn for last id

def last_lost_id():
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    last_id = 'SELECT * FROM lost_items WHERE id=(SELECT max(id) FROM lost_items)'
    if not isinstance(last_id, int):
        return 0
    x = c.execute(last_id)
    for bar in x:
        return bar[0]

def last_found_id():
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    last_id = 'SELECT * FROM found_items WHERE id=(SELECT max(id) FROM found_items)'
    if not isinstance(last_id, int):
        return 0
    x = c.execute(last_id)
    for bar in x:
        return bar[0]

#add lost item to database
def add_lost_item(user, item, category, date, location, description):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    item_id = last_lost_id() + 1
    lost_items_vals = [item_id, item, description, category, user, location, 40.7589, 73.985, date]
    c.execute("INSERT INTO lost_items (id, item, description, category, account_id, location, lat, long, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", lost_items_vals)
    ##appending lost item
    a = 'SELECT username, l_lost FROM users'
    x = c.execute(a)
    for bar in x:
        if(user == bar[0]):
            wow = bar[1]
            if wow == "":
                wow = str(item_id)
            else:
                wow+= "," + str(item_id)
            c.execute("UPDATE users SET l_lost='" + wow + "' WHERE username = '" + user + "'")
    db.commit()
    db.close()

#add found item to database
def add_found_item(user, item, category, date, location, description):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    item_id = last_found_id() + 1
    found_items_vals = [item_id, item, description, category, user, location, 40.7589, 73.985, date]
    c.execute("INSERT INTO found_items (id, item, description, category, account_id, location, lat, long, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", found_items_vals)
    ##appending lost item
    a = 'SELECT username, l_found FROM users'
    x = c.execute(a)
    for bar in x:
        if(user == bar[0]):
            wow = bar[1]
            if not isinstance(wow, str):
                wow = str(item_id)
            else:
                wow+= "," + str(item_id)
            c.execute("UPDATE users SET l_found='" + wow + "' WHERE username = '" + user + "'")
    db.commit()
    db.close()
    
add_found_item("joyce", "house", "accessory", "06/08/2018", "Times Square", "I couldn't find the owner so I broke in. Lmk if its yours. Yellow with a wooden awning. 3 bedroom.")


def item_listings():
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT * FROM lost_items'
    x = c.execute(a)
    item_list = []
    for bar in x:
        item_id = bar[0]
        item_name = bar[1]
        item_desc = bar[2]
        item_lat = bar[6]
        item_long = bar[7]
        item_location = bar[5]
        item_date = bar[8]
        ##add vars for location string and date
        item = {}
        item['item_id'] = item_id
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

# add_item("joyce", "boot", "accessory", 0, 40.76, -73.99)
# add_item("joyce", "yaya", "accessory", 0, 40.76, -73.99)
# add_item("joyce", "hehe", "accessory", 0, 40.76, -73.99)
# add_item("joyce", "luppo", "accessory", 0, 40.76, -73.99)
# print(item_listings())
#lost_items('joyce')

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
