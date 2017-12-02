#!/usr/bin/env python3
import urllib
import smtplib
from email.mime.text import MIMEText
from flask import Flask
from flask import request
from urllib.parse import unquote

smtp_host = ''
smtp_user = ''
smtp_pw = ''

mail_sender = ''
mail_recipient = ''

app = Flask(__name__)

@app.route('/')
def entry_point():
    return 'Usage: Send a POST request to /mailer with the fields msg for the message and sub for the subject of the message.'

@app.route('/mailer', methods=['POST'])
def handle_request():
        message = unquote(request.form['msg'])
        subject = unquote(request.form['sub'])
        if message != '':
            if subject != '':
                send_mail(message, subject)
            else:
                return '!!! NO DATA IN FORM !!!'
        return 'Message successfully sent.'

def send_mail(msg, subj):

        message = MIMEText(msg, 'html');
        
        message['Subject'] = subj
        message['From'] = mail_sender
        message['To'] = mail_recipient
        
        smtp = smtplib.SMTP(smtp_host)
        smtp.login(smtp_user, smtp_pw)
        smtp.send_message(message)
        smtp.quit()


