#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib


class CommonConfig(object):
    API_HEADERS = {'Content-type': 'application/json'}
    SMTP_SENDER = "akj2996@daum.net"
    SMTP_ADDR = "smtp.daum.net"
    SMTP_PORT = 465
    SMTP_LOGIN_ID = "akj2996"
    SMTP_LOGIN_PW = "deepir12!@"


class DevelopmentConfig(CommonConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/kaistdb'
    #SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@192.168.0.15/kaistdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FILE_PATH = 'c:\\project\\neuraltech\\'

class ProductionConfig(CommonConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p@ssw0rd@127.0.0.1/kaistdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEARCH_API_URL = 'http://127.0.0.1:6050'
    AUTH_URL = 'http://101.101.215.87:443/api/ext/auth'
    STATIC_FILE_PATH = '/data/neuraltech/frontend-vue/dist/'