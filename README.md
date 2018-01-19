# jazzy-ostriches - :mag_right: Lost in New York :mag:

#### Made by Alessandro Cartegni, Brian Leung, Dasha Shifrina, and Joyce Wu - SoftDev Pd. 7

![Our logo!](/static/logo-wide.png)

### Have you ever lost something in NYC?
Of course you have! With *__Lost in New York__*, never let that bother you again. Thanks to the kindness hidden deep down in the souls of all New Yorkers, any lost item that gets found will be yours once again. No longer will you need to retrace your steps or rummage through dirty lost and found bins when someone is safekeeping your item just for you! When you see something that belong to you on the map, just claim it and arrange via provided email contact when to get it back!

### Overview:
Lost in New York uses the Google Maps API, Lost and Found API, and Mailjet API to make an interactive "Lost and Found" for NYC. Users will be able to post both items that they have lost or found and it will show up as a map marker or item listing, with a corresponding description of the item. Users will then be able to contact the owner of the lost/found listing via email.

### How to procure API keys:
* #### Google Maps:
  1. Go to https://developers.google.com/maps/
  2. Select the "Google Maps JavaScript API"
  3. Click "Get A Key"
  4. Follow popup instructions
  5. Copy the key into keys.txt
* #### Mailjet:
  1. Go to https://dev.mailjet.com/ and sign up for an account.
  2. Activate your account via verification email.
  3. Go to the "My Account" tab
  4. Go to "REST API" and select "Master API & Sub API key management"
  5. You will see the public and private keys.
  6. Copy them into keys.txt
* #### Lost and Found:
  1. Go to https://www.lostandfound.com/api and sign up to request a key
  2. Follow the instructions to get a key
  3. Copy the key into keys.txt
### How to install the pip packages:

requirements.txt contains all the names of the dependencies needed.

Includes: <b>requests, mailjet_rest, sqlite3, flask, urllib2, json</b>

- Make sure requirements.txt is present
- Run this command: <b> `$ pip install -r requirements.txt`</b>

## How to run the application:
- <b>`$ python app.py`</b>
