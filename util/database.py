import sqlite3
import random

# only has login functionality so far

#fxns available: getting users, adding users, getting user's lost items, adding lost item to user account



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
    db = sqlite3.connect("/data/lost_and_found.db")
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



#add lost item to database
def add_item(user, item, category, date, location, description):
    db = sqlite3.connect("/data/lost_and_found.db")
    c = db.cursor()
    item_id = random.randint(1,24324342) #make this better l8r
    lost_items_vals = [item_id, item, description, category, user, 40.7589, 73.985]
    c.execute("INSERT INTO lost_items (id, item, description, category, account_id, lat, long) VALUES(?, ?, ?, ?, ?, ?, ?)", lost_items_vals)
    ##appending lost item
    a = 'SELECT username, l_lost FROM users'
    x = c.execute(a)
    for bar in x:
        if(user == bar[0]):
            wow = bar[1]
            wow+= "," + str(item_id)
            c.execute("UPDATE users SET l_lost='" + wow + "' WHERE username = '" + user + "'")
    db.commit()
    db.close()

#add_item("joyce", "dog", "accessory", "5/12/2008", "Times Square", "where is it")

#lost_items('joyce')

'''
# execute this file to create the initial database
if __name__ == '__main__':
    # initialize database
    db = sqlite3.connect("/data/lost_and_found.db")
    c = db.cursor()
    # table for user login
    c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, pass TEXT, l_found TEXT, l_lost TEXT);")
    #table with postings for lost items
    c.execute("CREATE TABLE lost_items (id INT, item TEXT, description TEXT, category TEXT, account_id INT, lat FLOAT, long FLOAT);")
    #table with postings for found items
    c.execute("CREATE TABLE found_items (id INT, item TEXT, description TEXT, category TEXT, account_id INT, lat FLOAT, long FLOAT);")
    db.commit()
    db.close()'''
