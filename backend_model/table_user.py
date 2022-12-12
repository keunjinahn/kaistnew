# -*- coding: utf-8 -*-
print ("module [backend_model.table_user.py] loaded")

from backend_model.database import DBManager
import datetime
db = DBManager.db

class Users(db.Model):
    __tablename__ = 'tb_users'

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.datetime.now)
    updated = db.Column('updated', db.DateTime)
    user_id = db.Column('user_id', db.String(48))
    user_pw = db.Column('user_pw', db.String(256))
    user_name = db.Column('user_name', db.String(48))
    user_type = db.Column('user_type', db.Integer, default=2)  # 1:Admin, 2:User
    user_status = db.Column('user_status', db.Integer, default=1)  # 1:Active, 2:Deactive
    company = db.Column('company', db.String(48))
    phone = db.Column('phone', db.String(30))
    email = db.Column('email', db.String(48))
    token = db.Column('token', db.String(128))  # added
    last_logon_time = db.Column('last_logon_time', db.DateTime)
    fk_vendor_id = db.Column('fk_vendor_id', db.Integer)
    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "user_id": self.user_id
            , "user_name": self.user_name
            , "user_type": self.user_type
            , "user_status": self.user_status
            , "phone": self.phone
            , "email": self.email
            , "last_logon_time": self.last_logon_time
            , "token": self.token
        }
        return resultJSON


class AccessHistory(db.Model):
    __tablename__ = 'tb_access_history'

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.datetime.now)
    user_id = db.Column('user_id', db.String(48))
    type = db.Column('type', db.Boolean)  # 0:로그인, 1:로그아웃
    update_time = db.Column('update_time', db.DateTime)  # 사용자 접속 시간
    ip_addr = db.Column('ip_addr', db.String(20))  # 사용자 접속IP
    os_ver = db.Column('os_ver', db.String(48))  # 사용자 접속 OS버전
    browser_ver = db.Column('browser_ver', db.String(48))  # 사용자 접속 브라우져 버전
    fk_user_id = db.Column('fk_user_id', db.Integer, db.ForeignKey(Users.id))
    user = db.relationship('Users')
    fk_vendor_id = db.Column('fk_vendor_id', db.Integer)
