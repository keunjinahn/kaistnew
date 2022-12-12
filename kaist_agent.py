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
config = read_from_file('./config.ini', 'INFO')
DATA_PATH = config['DATA_PATH']
AGENT_TYPE  = config['AGENT_TYPE']
DBSERVER_IP  = config['DBSERVER_IP']
AGENT_NUM  = config['AGENT_NUM']
print("DATA_PATH :",DATA_PATH,",AGENT_TYPE :",AGENT_TYPE,",AGENT_NUM:",AGENT_NUM,",DBSERVER_IP :",DBSERVER_IP)

class KaistAgent(object):
    def __init__(self, logger=None):
        file_logger = logging.getLogger("KaistAgent")
        file_logger.setLevel(logging.INFO)
        file_handler = handlers.RotatingFileHandler(
            "KaistAgent.log",
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
        self.logger.info("KaistAgent start1...")
        self.db = None
        self.capture_idx = 0
        return

    def connect_to_db(self):
        try:
            self.db = MySQLdb.connect(
                host=DBSERVER_IP,
                user='dbadmin',
                passwd='p@ssw0rd',
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

    def proc_sensors(self):
        if not self.connect_to_db():
            self.logger.error("Database initialize failed. Exit.")
            return False
#         try :
        data_files = glob(DATA_PATH + '*.*')
        for index,filepath in enumerate(data_files):
            print("filepath name :",filepath)
            file_name = os.path.basename(filepath)
            sql_isexist = "SELECT * FROM tb_sensor_files WHERE file_names='{0}' AND sensor_type='{1}' AND sensor_num={2} ".format(file_name,AGENT_TYPE,int(AGENT_NUM))
            print("sql_isexist :",sql_isexist)
            cursor = self.get_cursor()
            cursor.execute(sql_isexist)
            recv_data = [row for row in cursor.fetchall()]
            if len(recv_data) == 0 :
                sql_insert = '''
                    INSERT INTO tb_sensor_files(file_names,sensor_type,sensor_num,created_date) values('{0}','{1}',{2},now())
                    '''.format(file_name,AGENT_TYPE,int(AGENT_NUM))
                cursor.execute(sql_insert)
                cursor.execute(sql_isexist)
                recv_data = [row for row in cursor.fetchall()]
                fk_sensor_file_id = recv_data[0]['id']
                with open(filepath, 'r') as f:
                    if AGENT_TYPE == 'INJECTION':
                        for index,line in enumerate(f.readlines()) :
                            if index == 0 :
                                continue
                            line = line.replace("\n",'')
                            print("line : ",line)
                            obj = {
                                "msg":str(line)
                            }
                            data_msg = json.dumps(obj)
                            sql_insert_data = '''
                                INSERT INTO tb_sensor_data(data_msg,created_date,fk_sensor_file_id) values('{0}',now(),'{1}')
                                '''.format(data_msg,fk_sensor_file_id)
                            cursor.execute(sql_insert_data)
                    elif AGENT_TYPE == 'CNCOSCI':
                        data_list = []
                        for index,line in enumerate(f.readlines()) :
                            line = line.replace("\n",'')
                            print("line : ",line)
                            data_list.append(line)
                        obj = {
                            "msg":data_list
                        }
                        data_msg = json.dumps(obj)
                        sql_insert_data = '''
                            INSERT INTO tb_sensor_data(data_msg,created_date,fk_sensor_file_id) values('{0}',now(),'{1}')
                            '''.format(data_msg,fk_sensor_file_id)
                        cursor.execute(sql_insert_data)
#         except :
#             self.disconnect()
#             print("proc_sensors Exception!!")
        self.disconnect()

    def getURL(self,a_idx,t_idx,channel,date):
        return "http://mywatt.org/api/data_daily.php?a_idx={0}&t_idx={1}&ch_idx={2}&date={3}".format(a_idx,t_idx,channel,date)

    def proc_power(self,today):
        if not self.connect_to_db():
            self.logger.error("Database initialize failed. Exit.")
            return False
        AGENT_TYPE = "POWER"
        AGENT_NUM = 1
        value_set = {}
        for data in DATA_SET:
            if data['use'] == True:
                value_set[data['d_idx']] = []
                for ch_idx in range(data['ch_count']):
                    print("ch_idx :", ch_idx+1)
                    url = self.getURL(data['a_idx'],data['t_idx'],ch_idx+1, today)
                    result = json.loads(requests.get(url, verify=False).text)
                    if result["code"] == 200 :
                        value_set[data['d_idx']].append({
                            str(ch_idx):result['data'][today]
                        })
#         print(value_set)

        sqls = []
        cursor = None
        cursor = self.get_cursor()
        def conv_(v):
            date_time = "{0}:{1}:00".format(v['h'],v['m'])
            obj = {
                "date_time":date_time,
                "w":v['w']
            }
            return obj

        for data in DATA_SET:
            if data['use'] == True:
                sensors_msg = value_set[data['d_idx']]
                msg_list = map(lambda v:conv_(v),sensors_msg[0]['0'])
                m_array = [m for m in msg_list]
                s_m_array = sorted(m_array,key=lambda d:d['date_time'])
                print("m_array :",s_m_array)
#                 obj = {
#                     "msg":json.dumps(sensors_msg)
#                 }
                data_msg = json.dumps(s_m_array)
                sql_isexist = "SELECT * FROM tb_sensor_files WHERE file_names='{0}' AND sensor_type='{1}' AND sensor_num={2} ".format(today,AGENT_TYPE,int(AGENT_NUM))
                cursor = self.get_cursor()
                cursor.execute(sql_isexist)
                recv_data = [row for row in cursor.fetchall()]
                if len(recv_data) == 0 :
                    sql_insert = '''
                        INSERT INTO tb_sensor_files(file_names,sensor_type,sensor_num,created_date) values('{0}','{1}',{2},now())
                        '''.format(today,AGENT_TYPE,int(AGENT_NUM))
                    cursor.execute(sql_insert)
                    cursor.execute(sql_isexist)
                    recv_data = [row for row in cursor.fetchall()]
                    fk_sensor_file_id = recv_data[0]['id']
                    sql_insert_data = '''
                        INSERT INTO tb_sensor_data(data_msg,created_date,fk_sensor_file_id) values('{0}',now(),'{1}')
                        '''.format(data_msg,fk_sensor_file_id)
                    cursor.execute(sql_insert_data)
                else :
                    cursor.execute(sql_isexist)
                    recv_data = [row for row in cursor.fetchall()]
                    fk_sensor_file_id = recv_data[0]['id']
                    sql_insert_data = '''
                        UPDATE tb_sensor_data SET data_msg='{0}' WHERE fk_sensor_file_id={1}
                        '''.format(data_msg,fk_sensor_file_id)
                    cursor.execute(sql_insert_data)
        if cursor is not None:
            cursor.close()
        self.disconnect()

    def run(self):
        print("KaistAgent run...")
        self.proc_sensors()
        now = datetime.now()
        print("now : ",now.strftime("%Y%m%d"))
        self.proc_power(now.strftime("%Y%m%d"))


if __name__ == "__main__":
    app = KaistAgent(logger=None)
    app.run()

