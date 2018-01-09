import requests

def sendmail(losterID,finderID,lostItemID):
	headers = {'Content-Type': 'application/json',}
	
	data = '''{"Messages":[{
	"From":{"Email": "%s","Name": "%s"},
	"To": [{"Email": "%s","Name":"%s"}],
	"Subject": "MY FIRST EMAIL",
	"TextPart": "Greetings from Mailjet."}]}'''%()
	
	response = requests.post('https://api.mailjet.com/v3.1/send', headers=headers, data=data, auth=('PUBKEY', 'PRIVKEY'))
	print response
	
def formatMail(lostItemID,)

sendmail(...)