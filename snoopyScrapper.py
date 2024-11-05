import requests
from bs4 import BeautifulSoup, Tag
from datetime import date

#Gmail API imports
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

emailList = "" #add email or phone number email for txt messages
sender = "Snoopy Tracker <@gmail.com>" #add email for the sender
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

userAgent ={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"} 
snoopyPjs = "https://www.ae.com/us/en/p/women/loungewear-pjs/pajamas-pj-sets/ae-peanuts-fall-pumpkin-plush-pj-set/0575_3236_119"
className = "_oos-label_1bn8o3" #the class name of the price description parent div

def extract_source(url):
    return requests.get(url, headers=userAgent)

def innerHTML(element: Tag):
    return element.encode_contents()

def checkEmpty(element: Tag):
    if len(element.contents) > 0:
        return True
    else:
        return False

def gmail_send_message(message_text):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    #message.set_content("This is automated draft mail")
    message = MIMEText(message_text, 'html')


    message["To"] = emailList
    message["From"] = sender
    message["Subject"] = "Snoopy Pjs Tracker"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

def create_sms_message(message, link):
   return """<!DOCTYPE html>
            <html>
            <body style="font-family:Calibri, serif; background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;">
                <p> """ + message + """ </p>
                <a href="""+link+""">Link</a>
            </body>
            </html>
            """

#grab snoopy pj html
r = extract_source(snoopyPjs)
#grab soup of html from url
soup = BeautifulSoup(r.content, 'html.parser')
#check if unavailable string exists anywhere
element1 = soup.find(string='Unavailable')

#Unavailable text exists, check element now
notInStock = False
if element1:
    #search for div element of price indicator
    element2 = soup.find("div", class_=className, string='Unavailable')
    #check if available
    notInStock = checkEmpty(element2)


if notInStock:
   print("not in stock")
    # gmail_send_message(create_sms_message("Product is not in stock", snoopyPjs))
else:
   print("in stock") 
    # gmail_send_message(create_sms_message("Product is in stock!!", snoopyPjs))






