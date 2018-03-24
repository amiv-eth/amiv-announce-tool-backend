#!/usr/bin/env python3
import urllib
import smtplib
import json
import requests
from InvalidUsage import InvalidUsage
from time import time
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
port = 587
required_group = ''

app = Flask(__name__)

@app.route('/')
def entry_point():
    raise InvalidUsage('Wrong ressource', 400)

@app.route('/mailer', methods=['POST'])
def handle_request():
        message = unquote(request.form['msg'])
        subject = unquote(request.form['sub'])
        token = unquote(request.form['token'])

        if check_auth(token) == False:
                raise InvalidUsage('Unauthorized', 401)

        if message != '':
            if subject != '':
                before = time()
                send_mail(message, subject)
                took = time() - before
            else:
                raise InvalidUsage('Subject must not be empty!', 400)
        else:
                raise InvalidUsage('Message must not be empty!', 400)

        return '{"_status":"OK", "_code":200, "took":' + str(took) + ', "message":"E-Mail successfully sent."}'

def send_mail(msg, subj):

        message = MIMEText(msg, 'html');
        
        message['Subject'] = subj
        message['From'] = mail_sender
        message['To'] = mail_recipient
        
        try:
            smtp = smtplib.SMTP(smtp_host, port)
            smtp.login(smtp_user, smtp_pw)
            smtp.send_message(message)
        except:
            raise InvalidUsage('SMTP host or credentials misconfigured.', 500)

        smtp.quit()

def check_auth(token):
        group_met = False
        
        header = {"Authorization":token}

        try:
            api = requests.get(api_addr + '/groupmemberships', headers=header)
        except:
            raise InvalidUsage('AMIV-API address misconfigured or unreachable', 500)

        try:
            string = api.text
            obj = json.loads(string)
        
            content = obj['_items']

            for i in range(0, obj['_meta']['total']):
                if str(content[i]['_id']) == required_group:
                    group_met = True
                    break

        except KeyError:
            if str(obj["_status"]) == "ERR":
                if obj["_error"]["code"] == 401:
                    raise InvalidUsage('Invalid or expired token.', 401)
            else:
                raise InvalidUsage('AMIV-API returned unknown response.', 500)
        except:
            raise InvalidUsage('AMIV-API returned unknown response.', 500)

        return group_met
       

@app.errorhandler(InvalidUsage)
def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


@app.route('/englishman')
def teapot():
    raise InvalidUsage('I\'m a teapot', 418)
