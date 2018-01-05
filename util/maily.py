import requests

def mailsendtest():
	headers = {'Content-Type': 'application/json',}
	data = '{"Messages":[{"From":{"Email": "bleung@stuy.edu","Name": "Me"},"To": [{"Email": "brianleung329@gmail.com","Name":"Brian"}],"Subject": "My first Mailjet Email!","TextPart": "Greetings from Mailjet."}]}'
	response = requests.post('https://api.mailjet.com/v3.1/send', headers=headers, data=data, auth=('PUBLIC', 'PRIVATE'))
	print response

mailsendtest()