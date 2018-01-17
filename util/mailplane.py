from mailjet_rest import Client
import csv, sqlite3

# Gets API keys for Mailjet
# 0 gets private, anything else gets public.
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

def sendMail(ownData, userData):
	API_SECRET = getKey(0)
	API_KEY = getKey(1)

	print(API_KEY)
	print(API_SECRET)

	mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')

	data = {
	    'FromEmail': 'bleung@stuy.edu',
	    'FromName': 'Lost In New York',
	    'Subject': 'Something Has Been Found! - Lost In New York',
	    'Text-part': 'Your lost Item has been found',
	    'Html-part': '<h3>Dear passenger, welcome to Mailjet!</h3><br />May the delivery force be with you!',
	    'Recipients': [{'Email':'brianleung329@gmail.com'}]
	}

	result = mailjet.send.create(data=data)
	print result.status_code
	print result.json()

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

print getUserData(1)
print getItemData(1,0)


