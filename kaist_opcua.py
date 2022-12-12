# -*- coding:utf-8 -*-
# 한글 주석 처리
__author__ = 'bychem'

import logging
import time
import json
import os
import sys
import platform
from logging import handlers
import signal
import json
from scapy.all import *
import MySQLdb
from configparser import ConfigParser
from glob import glob
import requests
from datetime import datetime, timedelta
from opcua import Client
from opcua import ua
import random


protocols = {1:'ICMP',6:'TCP',17:'UDP'}


DATA_SET = [
    {"d_idx":"210272","a_idx":945,"t_idx":998,"ch_count":1,"name":"B","use":True},
]

def read_from_file(filename, section, required_props=None):
    config_parser = ConfigParser()
    print("config_parser : ", config_parser)
    config_parser.optionxform = str
    data = dict()

    try:
        data_set = config_parser.read(filename)
        print("data_set : ",data_set)
        if len(data_set) == 0:
            return None

        if section not in config_parser.sections():
            return dict()

        for k, v in config_parser.items(section):
            data[k] = v

        return data

    except:
        print("read_from_file Open  file failed ")
        return None

config = None
config = read_from_file('./config_osci.ini', 'INFO')
DATA_PATH = config['DATA_PATH']
AGENT_TYPE  = config['AGENT_TYPE']
DBSERVER_IP  = config['DBSERVER_IP']
AGENT_NUM  = config['AGENT_NUM']
OPCUA_TEST = int(config['OPCUA_TEST'])
OPCUA_INTERVAL = int(config['OPCUA_INTERVAL'])
OPCUA_USE_1 = int(config['OPCUA_USE_1'])
OPCUA_USE_2 = int(config['OPCUA_USE_2'])
OPCUA_CSTRING_1 = config['OPCUA_CSTRING_1']
OPCUA_CSTRING_2 = config['OPCUA_CSTRING_2']
POWER_DATA_PATH = config['POWER_DATA_PATH']
POWER_USE_1 = int(config['POWER_USE_1'])
POWER_1_IP = config['POWER_1_IP']
print("DATA_PATH :",DATA_PATH,",AGENT_TYPE :",AGENT_TYPE,",AGENT_NUM:",AGENT_NUM,",DBSERVER_IP :",DBSERVER_IP)
print("POWER_DATA_PATH :",POWER_DATA_PATH,",POWER_USE_1 :",POWER_USE_1,",POWER_1_IP:",POWER_1_IP)

class KaistOpcua(object):
    def __init__(self, logger=None):
        file_logger = logging.getLogger("KaistOpcua")
        file_logger.setLevel(logging.INFO)
        file_handler = handlers.RotatingFileHandler(
            "KaistOpcua.log",
            maxBytes=(1024 * 1024 * 1),
            backupCount=5
        )

        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s in [%(filename)s:%(lineno)d](%(process)d)')
        file_handler.setFormatter(formatter)
        file_logger.addHandler(file_handler)
        logger = file_logger
        if logger is None:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('KaistAgent')
        else:
            self.logger = logger
        self.api_headers = {'Content-type': 'application/json'}
        self.logger.info("KaistOpcua start1...")
        self.db = None
        self.capture_idx = 0
        self.is_running = True
        self.opcua_server_1 = None
        self.opcua_server_2 = None
        return

    def connect_to_db(self):
        try:
            self.db = MySQLdb.connect(
                host=DBSERVER_IP,
                user='dbadmin',
                passwd='p#ssw0rd',
                db='kaistdb',
                charset='utf8',
                use_unicode=True
            )
            self.db.autocommit(True)
            return True

        except:
            print('Database connection failed')

            return False

    def disconnect(self):
        if self.db:
            self.db.close()

    def get_cursor(self):
        if self.db is None:
            return None

        return self.db.cursor(MySQLdb.cursors.DictCursor)

    def init_signal_handler(self):
        def signal_term_handler(signum, frame):
            self.logger.info("Got TERM signal. Stopping agent.")
            self.stop_agent()

        signal.signal(signal.SIGTERM, signal_term_handler)

    def proc_opcua(self,opcua_server,sensor_num):
        now = datetime.now()
        use_crypto = False

        cursor = self.get_cursor()
        try:

            sTimeStamp = ''
            sValue = ''
            if OPCUA_TEST == 0 :
                #client.set_user("kaist")
                #client.set_password("kaist")
                opcua_server.load_type_definitions()  # load definition of server specific structures/extension objects
                # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
                root = opcua_server.get_root_node()
                objects = opcua_server.get_objects_node()
                var = opcua_server.get_node("ns=4;s=CH0_RAW_DATA")
                varObj = var.get_data_value()
                print("timestamp : ", varObj.SourceTimestamp,",Value : ", varObj.Value._value,",obj:",varObj.Value)
                sTimeStamp = str(varObj.SourceTimestamp)
                sValue = str(varObj.Value._value)
                #timestamp :  2021-06-28 11:49:43.049000 ,Value :  -2 ,obj: Variant(val:-2,type:VariantType.Int16)

            else :
                sTimeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
                sValue = round(random.uniform(30.0,80.0), 1)
            
            file_name = '{0}.csv'.format(now.strftime("%Y%m%d"))
            sql_isexist = "SELECT * FROM tb_sensor_files WHERE file_names='{0}' AND sensor_type='CNCOSCI' AND sensor_num={1} ".format(file_name,int(sensor_num))
            print("sql_isexist :",sql_isexist)
            cursor.execute(sql_isexist)
            recv_data = [row for row in cursor.fetchall()]
            print("recv_data 1:",recv_data)
            if len(recv_data) == 0 :
                sql_insert = '''
                    INSERT INTO tb_sensor_files(file_names,sensor_type,sensor_num,created_date) values('{0}','CNCOSCI',{1},now())
                    '''.format(file_name,int(sensor_num))
                print("sql_insert :",sql_insert)
                cursor.execute(sql_insert)
                cursor.execute(sql_isexist)
                recv_data = [row for row in cursor.fetchall()]
                print("recv_data 2:",recv_data)
            fk_sensor_file_id = recv_data[0]['id']
            print("fk_sensor_file_id :",fk_sensor_file_id)
            line = '{0},{1}'.format(sTimeStamp,sValue)
            print("line :",line)
            obj = {
                "msg":str(line)
            }
            data_msg = json.dumps(obj)
            sql_insert_data = '''
                INSERT INTO tb_sensor_data(data_msg,created_date,fk_sensor_file_id) values('{0}',now(),'{1}')
                '''.format(data_msg,fk_sensor_file_id)
            cursor.execute(sql_insert_data)
        except:
            print("opcua connect except!")
            self.capture_idx = 300
            pass
        finally:
            pass

        self.capture_idx += 1

    def proc_power(self,ipaddress,sensor_num):
        now = datetime.now()
        cursor = self.get_cursor()
        #try:
        sTimeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
        sValue = round(random.uniform(30.0,80.0), 1)
        file_name = '{0}_EA_{1}.txt'.format(ipaddress,now.strftime("%Y%m%d"))
        file_name_path = '{0}{1}'.format(POWER_DATA_PATH,file_name)
        
        print("file_name :",file_name_path)    
        with open(file_name_path,'r') as file_data_r :
            lines = file_data_r.readlines()

            sql_isexist = "SELECT * FROM tb_sensor_files WHERE file_names='{0}' AND sensor_type='POWER' AND sensor_num={1} ".format(file_name,int(sensor_num))
            print("sql_isexist :",sql_isexist)
            cursor.execute(sql_isexist)
            recv_data = [row for row in cursor.fetchall()]
            print("recv_data 1:",recv_data)
            if len(recv_data) == 0 :
                sql_insert = '''
                    INSERT INTO tb_sensor_files(file_names,sensor_type,sensor_num,created_date) values('{0}','POWER',{1},now())
                    '''.format(file_name,int(sensor_num))
                print("sql_insert :",sql_insert)
                cursor.execute(sql_insert)
                cursor.execute(sql_isexist)
                recv_data = [row for row in cursor.fetchall()]
                print("recv_data 2:",recv_data)

            fk_sensor_file_id = recv_data[0]['id']
            print("fk_sensor_file_id :",fk_sensor_file_id)

            
            sql_islast = "SELECT created_date FROM tb_sensor_data WHERE fk_sensor_file_id={0} order by id desc limit 1 ".format(fk_sensor_file_id)
            print("sql_islast :",sql_islast)
            cursor.execute(sql_islast)
            recv_data = [row for row in cursor.fetchall()]
            print("recv_data 1:",recv_data)
            last_date = datetime.now()
            if len(recv_data) != 0 :
                print("recv_data[0]['created_date'] :, ",recv_data[0]['created_date'])
                last_date = recv_data[0]['created_date']
            
            line = '{0},{1}'.format(sTimeStamp,sValue)
            for line in lines :
                lineArray = line.split(',')
                timeArray = lineArray[0].split('-')
                strNow = "{0}-{1}-{2} {3}:{4}:{5}".format(timeArray[0],timeArray[1],timeArray[2],timeArray[3],timeArray[4],timeArray[5])
                if last_date  >= datetime.strptime(strNow,'%Y-%m-%d %H:%M:%S') :
                    continue
                print("line :",line)
                obj = {
                    "msg":str(line)
                }
                data_msg = json.dumps(obj)
                sql_insert_data = '''
                    INSERT INTO tb_sensor_data(data_msg,created_date,fk_sensor_file_id) values('{0}','{1}','{2}')
                    '''.format(data_msg,strNow,fk_sensor_file_id)
                cursor.execute(sql_insert_data)
        # except:
        #     print("opcua connect except!")
        #     pass
        # finally:
        #     pass

        self.capture_idx += 1        

    def init_signal_handler(self):
        def signal_term_handler(signum, frame):
            self.logger.info("Got TERM signal. Stopping agent.")
            self.stop_agent()

        signal.signal(signal.SIGTERM, signal_term_handler)

    def run(self):
        print("KaistOpcua run...")
        self.init_signal_handler()

        while self.is_running:
            if self.capture_idx >= 300:
                if self.get_cursor() is not None :
                    self.disconnect()
                if not self.connect_to_db():
                    self.logger.error("Database initialize failed. Exit.")
                    self.capture_idx = 0
                    return

                try :
                    if OPCUA_USE_1 == 1:
                        # if self.opcua_server_1 is not None:
                        #     self.opcua_server_1.disconnect()
                        self.opcua_server_1 = Client(OPCUA_CSTRING_1)
                        self.opcua_server_1.connect()
                except :
                    print("opcua server 1 connect except!")
                    sys.exit(0)

                try :
                    if OPCUA_USE_2 == 1:
                        # if self.opcua_server_2 is not None :
                        #     self.opcua_server_2.disconnect()
                        self.opcua_server_2 = Client(OPCUA_CSTRING_2)
                        self.opcua_server_2.connect()
                except :
                    print("opcua server 2 connect except!")
                    sys.exit(0)
                self.capture_idx = 0

            
            # if OPCUA_USE_1 == 1 :
            #     self.proc_opcua(self.opcua_server_1,1)
            # if OPCUA_USE_2 == 1 :
            #     self.proc_opcua(self.opcua_server_2,2)
            
            if POWER_USE_1 == 1 :
                self.connect_to_db()
                self.proc_power(POWER_1_IP,1)

            print("capture_idx : ",self.capture_idx)


            for _ in range(OPCUA_INTERVAL):
                if self.is_running:
                    time.sleep(1)

        if self.get_cursor() is not None:
            self.disconnect()
            if OPCUA_USE_1 == 1 and self.opcua_server_1 is not None:
                self.opcua_server_1.disconnect()
            if OPCUA_USE_2 == 1 and self.opcua_server_2 is not None:
                self.opcua_server_2.disconnect()

if __name__ == "__main__":
    app = KaistOpcua(logger=None)
    app.run()

