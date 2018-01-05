import requests

def mailsendtest():
	import requests

	headers = {
    	'Content-Type': 'application/json',
	}
	response = requests.post('https://api.mailjet.com/v3.1/send', headers=headers, auth=('$MJ_APIKEY_PUBLIC', '$MJ_APIKEY_PRIVATE'))


