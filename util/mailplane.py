'''
JAZZY OSTRICHES:
SOFTDEV FINAL PROJECT:
LOST IN NEW YORK
'''
from mailjet_rest import Client
import csv, sqlite3

# Gets API keys for Mailjet
# 0 gets private, anything else gets the public.
def getKey(keytype):
	if (keytype==0):
		N = 5
	else:
		N = 3
	with open('../keys.txt', 'rb') as passport:
		reader = csv.reader(passport)
		for i, row in enumerate(reader):
			if i == N:
				return row[0]
	print "ERROR: missing file?"
	return 1

#Will send the email from the user with ownID to the owner of item with itemID
#ownID: ID of sender
#itemID: ID of item
#itemLostOrFound: Whether item is in lost or found table
def sendMail(ownID, itemID, itemLostOrFound):
	API_SECRET = getKey(0)
	API_KEY = getKey(1)

	print(API_KEY)
	print(API_SECRET)
	
	mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')
	sender = getUserData(ownID)
	item = getItemData(itemID,itemLostOrFound)
	receiver = getUserData(item["itemOwner"])
	data = {
	    'FromEmail': "bleung@stuy.edu",
	    'FromName': 'Lost In New York - %s'%(str(sender["username"])),
	    'Subject': 'About the item: %s'%(str(item["itemName"])),
	    'Text-part': 'Your lost Item has been found',
	    'Html-part': '<h3>%s wants to contact you about %s!</h3><br />YAY!<br />Please message %s about this item'%(str(sender["username"]),str(item["itemName"]),str(sender["email"])),
	    'Recipients': [{'Email':str(receiver["email"])}]
	}
	print str(receiver["email"])
	result = mailjet.send.create(data=data)
	print result.status_code
	print result.json()
	print sender
	print item
	print receiver

#Will return a dictionary of info about a lost or found item.
#itemID: ID of item
#lostOrFound: Whether to look in the lost or found table
#{"itemName":name of item,"itemDesc":item description, "itemOwner":ID of owner of item}
#Note: lostOrFound takes an integer.
#	   If lostOrFound = 0, it will search through the "lost_items" table
#	   Else, it will search through the "found_items" table
def getItemData(itemID,lostOrFound):
	if lostOrFound == 0:
		itemStatus = "lost_items"
	else:
		itemStatus = "found_items"
	cmd = "SELECT * FROM %s WHERE id=%i"%(itemStatus,itemID)
	db_name = "../data/lost_and_found.db"
	dab = sqlite3.connect(db_name)
	c = dab.cursor()
	itemRawData = c.execute(cmd)
	itemDict = {}
	for itemData in itemRawData:
		itemDict["itemName"]=itemData[1]
		itemDict["itemDesc"]=itemData[2]
		itemDict["itemOwner"]=itemData[4]
	return itemDict

#Will return a dictionary of info about a user
#userID: ID of user
#{"username":username,"email":email of user}
def getUserData(userID):
	cmd = "SELECT * FROM users WHERE id=%i"%(userID)
	db_name = "../data/lost_and_found.db"
	dab = sqlite3.connect(db_name)
	c = dab.cursor()
	users = c.execute(cmd)
	userDict = {}
	for userData in users:
		userDict["username"] = userData[1] 
		userDict["email"] = userData[2]
	return userDict

#print getUserData(1)
#print getItemData(1,0)
sendMail(4,2,0)
#sendVerificationEmail("Mank@bxscience.edu")
