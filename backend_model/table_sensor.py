# -*- coding: utf-8 -*-

print ("module [backend_model.table_patent.py] loaded")
from backend_model.database import DBManager
from backend_model.table_user import Users
import datetime

db = DBManager.db


class SensorFiles(db.Model):
    __tablename__ = 'tb_sensor_files'

    id = db.Column('id', db.Integer, primary_key=True)
    file_names = db.Column('file_names', db.String(50))
    sensor_type = db.Column('sensor_type', db.String(50))
    sensor_num = db.Column('sensor_num', db.Integer)
    created_date = db.Column('created_date', db.DateTime, default=datetime.datetime.now)

class SensorData(db.Model):
    __tablename__ = 'tb_sensor_data'
    id = db.Column('id', db.Integer, primary_key=True)
    data_msg = db.Column('data_msg', db.String(65535))
    fk_sensor_file_id = db.Column('fk_sensor_file_id', db.Integer)
    created_date = db.Column('created_date', db.DateTime, default=datetime.datetime.now)

class TB_VENDOR(db.Model):
    __tablename__ = 'tb_vendor'

    id = db.Column('id', db.Integer, primary_key=True)
    vendor_id = db.Column('vendor_id', db.String(128))
    vendor_name = db.Column('vendor_name', db.String(128))
    vendor_use = db.Column('vendor_use', db.Integer)
    active = db.Column('active', db.Integer)


class TB_SENSOR_UPLOAD(db.Model):
    __tablename__ = 'tb_sensor_upload'

    id = db.Column('id', db.Integer, primary_key=True)
    sender_ip = db.Column('sender_ip', db.String(128))
    company_id = db.Column('company_id', db.String(128))
    sensors_msg = db.Column('sensors_msg', db.String(2048))
    created_date = db.Column('created_date', db.DateTime)

