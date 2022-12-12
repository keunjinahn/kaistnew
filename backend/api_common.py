# -*- coding: utf-8 -*-
print ("module [backend.api_common] loaded")

import time
import smtplib
import hashlib
from flask import make_response, jsonify, request, json, Response, send_from_directory
from flask_restless import ProcessingException
from flask_restful import reqparse
from datetime import datetime
import os
import json

from backend import manager
from backend import app, login_manager
from backend_model.table_user import *
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_manager.user_loader
def load_user(id):
    user = DBManager.db.session.query(Users).get(id)
    return user


@app.route('/api/v1/login', methods=['POST'])
def login_api():
    data = json.loads(request.data)
    result = ''
    print("111")
    if data['username'] is not None and data['password'] is not None:
        loginuser = db.session.query(Users).filter(Users.user_id == data["username"]).first()

        if loginuser is None:
            result = {'status': False, 'reason': 1}  # ID 없음
        else:
            if loginuser.user_pw != password_encoder_512(data["password"]):
                result = {'status': False, 'reason': 2} # PW 틀림
                print("222")
            else:  # Login 성공
                if loginuser.user_status == 2:
                    result = {'status': False, 'reason': 3}  # Activation 안됨
                else:
                    print("333")
                    loginuser.last_logon_time = datetime.datetime.now()
                    loginuser.token = generate_token(data['username'])
                    db.session.query(Users).filter(Users.user_id == data["username"])\
                        .update(dict(last_logon_time=loginuser.last_logon_time, token=loginuser.token))

                    new_access_history = AccessHistory()
                    new_access_history.type = 0  # Login
                    user_agent = request.environ.get('HTTP_USER_AGENT')
                    new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(user_agent)
                    new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    new_access_history.update_time = datetime.datetime.now()
                    new_access_history.user_id = loginuser.user_id
                    new_access_history.FK_user_id = loginuser.id
                    db.session.add(new_access_history)
                    db.session.commit()

                    result = {'status': True, 'reason': 0, 'user': loginuser.serialize()}
    print("444:",result)
    return make_response(jsonify(result), 200)

@app.route("/api/v1/logout", methods=["POST"])
def logout_api():
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    result = ''
    if token is None:
        print("token is none")

    loginUser = Users.query.filter_by(token=token).first()
    if loginUser is None:
        print("user is none")
    else:
        new_access_history = AccessHistory()
        new_access_history.type = 1  # Logout
        userAgent = request.environ.get('HTTP_USER_AGENT')
        new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(userAgent)
        new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        new_access_history.update_time = datetime.datetime.now()
        new_access_history.user_id = loginUser.user_id
        new_access_history.fk_user_id = loginUser.id

        db.session.add(new_access_history)
        db.session.commit()

    return make_response(jsonify(result), 200)

def generate_token(userID):
    m = hashlib.sha1()

    m.update(userID.encode('utf-8'))
    m.update(datetime.datetime.now().isoformat().encode('utf-8'))

    return m.hexdigest()

def check_token(search_params=None, **kw):
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    if token is None:
        raise ProcessingException(description="Not Authorized", code=410)
    user = Users.query.filter_by(token=token).first()
    if user is None:
        raise ProcessingException(description="Not Authorized", code=411)

def check_token_single(search_params=None, **kw):
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]

    if token is None:
        raise ProcessingException(description="Not Authorized", code=410)

    user = Users.query.filter_by(token=token).first()
    if user is None:
        raise ProcessingException(description="Not Authorized", code=411)

def password_encoder_512(password):
    h = hashlib.sha512()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

def send_message(recipient, subject, message):
    sender = app.config["SMTP_SENDER"]

    headers = [
        "From: " + sender,
        "Subject: " + subject,
        "To: " + recipient,
        "MIME-Version: 1.0",
        "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    message = headers + '\r\n\r\n\r\n' + message

    # Send mail
    server = smtplib.SMTP_SSL(app.config["SMTP_ADDR"], app.config["SMTP_PORT"])
    #server.starttls()
    server.login(app.config["SMTP_LOGIN_ID"], app.config["SMTP_LOGIN_PW"])

    message = message.encode("ascii", errors="ignore")

    server.sendmail(sender, recipient, message)
    server.quit()

def get_os_browser_from_useragent(userAgent):
    os_ver = "Unknown"
    browser_ver = "Unknown"

    if userAgent.find("Linux") != -1:
        os_ver = "Linux"
    elif userAgent.find("Mac") != -1:
        os_ver = "MacOS"
    elif userAgent.find("X11") != -1:
        os_ver = "UNIX"
    elif userAgent.find("Win") != -1:
        os_ver = "Windows"

    if userAgent.find("MSIE 6") != -1:
        browser_ver = "Internet Explorer 6"
    elif userAgent.find("MSIE 7") != -1:
        browser_ver = "Internet Explorer 7"
    elif userAgent.find("MSIE 8") != -1:
        browser_ver = "Internet Explorer 8"
    elif userAgent.find("MSIE 9") != -1:
        browser_ver = "Internet Explorer 9"
    elif userAgent.find("MSIE 10") != -1:
        browser_ver = "Internet Explorer 10"
    elif userAgent.find("Trident") != -1 or userAgent.find("trident") != -1:
        browser_ver = "Internet Explorer 11"
    elif userAgent.find("Firefox") != -1:
        browser_ver = "Firefox"
    elif userAgent.find("Opera") != -1:
        browser_ver = "Opera"
    elif userAgent.find("Chrome") != -1:
        browser_ver = "Chrome"
    elif userAgent.find("Safari") != -1 or userAgent.find("Chrome") == -1:
        browser_ver = "Safari"
    elif userAgent.find("Edge") != -1 or userAgent.find("edge") != -1:
        browser_ver = "Microsoft Edge"

    return os_ver, browser_ver


def date_encoder(thing):
    list_date = str(thing).split(":")

    if hasattr(thing, 'isoformat'):
        if len(list_date[0]) == 1:
            return "0" + thing.isoformat()
        return thing.isoformat()
    else:
        if len(list_date[0]) == 1:
            return "0" + str(thing)
        return str(thing)


