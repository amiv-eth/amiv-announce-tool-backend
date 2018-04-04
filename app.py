#!/usr/bin/env python3

import smtplib, requests, config

from time import time
from json import loads
from flask import Flask
from flask import request
from flask import jsonify
from urllib.parse import unquote
from email.mime.text import MIMEText
from InvalidUsage import InvalidUsage

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

        message = MIMEText(msg, 'html')
        
        message['Subject'] = subj
        message['From'] = config.MAIL_SENDER
        message['To'] = config.MAIL_RECEIPIENT
        
        try:
            smtp = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
            smtp.starttls()
            smtp.login(config.SMTP_USER, config.SMTP_PASSWORD)
            smtp.send_message(message)
        except:
            raise InvalidUsage('SMTP host or credentials misconfigured.', 500)

        smtp.quit()

def check_auth(token):
        group_met = False

        try:
            api = requests.get(config.API_DOMAIN + '/groupmemberships?embedded={"group":1}', auth=requests.auth.HTTPBasicAuth(token, ''))
        except:
            raise InvalidUsage('AMIV-API address misconfigured or unreachable', 500)

        try:
            string = api.text
            obj = loads(string)
        
            content = obj['_items']

            for i in range(0, obj['_meta']['total']):
                if str(content[i]['group']['name']) == config.REQUIRED_GROUP:
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
