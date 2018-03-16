#!/usr/bin/env python3
import urllib
import smtplib
import json
import http.client
from email.mime.text import MIMEText
from flask import Flask
from flask import request
from flask import jsonify
from urllib.parse import unquote

smtp_host = ''
smtp_user = ''
smtp_pw = ''

mail_sender = ''
mail_recipient = ''

api_addr = 'http://amiv-api.ethz.ch'
required_group = ''

app = Flask(__name__)

@app.route('/')
def entry_point():
    return error(0)

@app.route('/mailer', methods=['POST'])
def handle_request():
        message = unquote(request.form['msg'])
        subject = unquote(request.form['sub'])
        token = unquote(request.form['token'])

        if(check_auth(token) == False)
                return error['401']

        if message != '':
            if subject != '':
                send_mail(message, subject)
            else:
                return error['...']
        else:
                return error['...']

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

def check_auth(token):
        api = http.client.HTTPConnection(api_addr)
        api.request('GET', '/groupmemberships', '', {"Authorization":token})
        
        resp = api.getresponse()
        
        string = resp.read().decode('ascii')
        obj = json.loads(string)
        
        content = obj['_items']

        group_met = False

        for i in range(0, obj['_meta']['total']):
            if(content[i] == required_group)
                group_met = True
                break

        return group_met
       

@app.errorhandler(InvalidUsage)
def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
