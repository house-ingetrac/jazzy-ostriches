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

#Gets user ID of a username
#If the function returns -1, the user does not exist
def getUserID(username):
	cmd = "SELECT * FROM users WHERE username='%s'"%(username)
	db_name = "../data/lost_and_found.db"
	dab = sqlite3.connect(db_name)
	c = dab.cursor()
	userRawData = c.execute(cmd)
	retval = -1
	for userArr in userRawData:
		retval = userArr[0]
	print retval
	return retval
	

#Will send the email from the user with selfUser to the owner of item with itemID
#selfUser: username of sender
#itemID: ID of item
#itemLostOrFound: Whether item is in lost or found table
def sendMail(selfUser, itemID, itemLostOrFound):
	API_SECRET = getKey(0)
	API_KEY = getKey(1)

	#print(API_KEY)
	#print(API_SECRET)
	
	mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')
	sender = getUserData(selfUser)
	item = getItemData(itemID,itemLostOrFound)
	receiver = getUserData(item["itemOwner"])
	data = {
	    'FromEmail': "bleung@stuy.edu",
	    'FromName': 'Lost In New York - %s'%(str(sender["username"])),
	    'Subject': 'About the item: %s'%(str(item["itemName"])),
	    'MJ-TemplateID': '296066',
	    'MJ-TemplateLanguage': 'true',
	    'Recipients': [
    	{
    		'Email':str(receiver["email"]),
    		'Vars':
    		{
    			"recvUser": str(receiver["username"]),
    			"recvEmail": str(sender["email"]),
    			"item": str(item["itemName"]),
    			"sendUser": str(sender["username"])
    		}
    	}
		]
	}

	result = mailjet.send.create(data=data)
	print result
	print result.json()


'''
	filters = {
    'EditMode': 'tool',
    'Limit': '100',
    'OwnerType': 'user'
	}
	result = mailjet.template.get(filters=filters)
	#print result.status_code
	print result.status_code
	print result.json()
	print sender
	print item
	print receiver
'''


#Will return a dictionary of info about a lost or found item.

#{"itemName":name of item,"itemDesc":item description, "itemOwner":ID of owner of item}

#itemID: ID of item
#lostOrFound: Whether to look in the lost or found table
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

#{"username":username,"email":email of user}

#userID: ID of user
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

#TESTING

#print getUserData(1)
#print getItemData(1,0)
#sendMail(4,2,0)
getUserID("brian")
#sendVerificationEmail("Mank@bxscience.edu")
