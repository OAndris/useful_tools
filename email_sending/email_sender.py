"""
Idea based on "Complete Python Developer in 2020: Zero to Mastery" from Andrei Neagoie.

NOTES (from Andrei):
In the case that you are sending emails through GMAIL, just go to your account(gmail) -> Account setting -> Scroll to the bottom of the page and you see Less Secured Apps tab ,now you just have to turn that feature ON. for more info visit this:
Links Less Secured Apps : https://support.google.com/accounts/answer/6010255
Third party sites & apps: https://support.google.com/accounts/answer/3466521
I recommend turning that feature back OFF once done experimenting with email.
"""


import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path


def construct_email(sender_name, receiver_email, subject):
    email = EmailMessage()
    email['from'] = sender_name
    email['to'] = receiver_email
    email['subject'] = subject
    return email


def add_content_plaintext(email):
    email.set_content('I am a Python Master!')
    return email


def add_content_html(email, html_variables, html_file='index.html'):
    html = Template(Path(html_file).read_text())
    email.set_content(html.substitute(html_variables), 'html')
    return email


def send_email(email, sender_email, send_password):
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender_email, send_password)
        smtp.send_message(email)
        print('Success!')


def main(sender_name, sender_email, send_password, receiver_email, subject, mode):
    email = construct_email(sender_name, receiver_email, subject)
    if mode == 'plaintext':
        email = add_content_plaintext(email)
    elif mode == 'html':
        email = add_content_html(email, html_variables, html_file='index.html')
    send_email(email, sender_email, send_password)





if __name__ == '__main__':
    html_variables = {'name': 'Tim'}
    main()
