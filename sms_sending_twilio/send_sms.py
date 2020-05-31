"""
Send custom SMS to any phone number, using Twilio.
"""

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = ''
auth_token = ''

msg = 'Happy Birthday!'
from_ = '+12345678901'
to = ''

client = Client(account_sid, auth_token)
message = client.messages.create(body=msg, from_=from_, to=to)
print(message.sid)
