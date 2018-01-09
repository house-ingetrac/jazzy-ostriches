from mailjet_rest import Client
import csv

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
	return "ERROR: missing file?"

#def popData(from_user,subject,)


API_SECRET = getKey(0)
API_KEY = getKey(1)

print(API_KEY)
print(API_SECRET)

mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')

data = {
    'FromEmail': 'bleung@stuy.edu',
    'FromName': 'Lost In New York',
    'Subject': 'Something Has Been Found! - Lost In New York',
    'Text-part': 'Your lost Iem has been found',
    'Html-part': '<h3>Dear passenger, welcome to Mailjet!</h3><br />May the delivery force be with you!',
    'Recipients': [{'Email':'brianleung329@gmail.com'}]
}

result = mailjet.send.create(data=data)
print result.status_code
print result.json()

