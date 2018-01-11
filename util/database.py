import sqlite3

# only has login functionality so far

# execute this file to create the initial database
if __name__ == '__main__':
    # initialize database
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    # table for user login
    c.execute("CREATE TABLE users (id INT, username TEXT, email TEXT, pass TEXT, l_found TEXT, l_lost TEXT")
    #table with postings for lost items
    c.execute("CREATE TABLE lost_items (id INT, item TEXT, description TEXT, category TEXT, account_id INT, lat FLOAT, long FLOAT")
    #table with postings for found items
    c.execute("CREATE TABLE lost_items (id INT, item TEXT, description TEXT, category TEXT, account_id INT, lat FLOAT, long FLOAT")
    db.commit()
    db.close()


# -----FUNCTIONS FOR LOGIN SYSTEM-----
# returns a dictionary for user data {user: pass}
def getUsers():
    db = sqlite3.connect("data/")
    c = db.cursor()
    a = 'SELECT user, pass FROM users'
    x = c.execute(a)
    users = {}
    for line in x:
        users[line[0]] = line[1]
    db.close()
    return users


# add the login to the database
def addUser(user, password):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    vals = [user, password]
    c.execute("INSERT INTO users VALUES(?, ?)", vals)
    db.commit()
    db.close()

# -----FUNCTIONS FOR ITEM SYSTEM-----

#print all lost items from user
def lost_items(user):
    db = sqlite3.connect("data/lost_and_found.db")
    c = db.cursor()
    a = 'SELECT username, itemSubs FROM items' #fix this
    x = c.execute(a)
    lost_items = {}
