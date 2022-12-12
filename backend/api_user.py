# -*- coding: utf-8 -*-
from backend import manager
from backend.api_common import *
from backend_model.table_user import *
from flask_restless import ProcessingException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("module [backend.api_user] loaded")

db = DBManager.db


def pre_check_duplicate_userid(instance_id=None, data=None, **kw):

    if "user_status" in data:
        if data['user_status'] == 2:
            pass
        else:
            check_token()
    else:
        check_token()

    if "user_pw" in data:
        data['user_pw'] = password_encoder_512(data['user_pw'])

    if "user_id" in data:
        chk_user = Users.query.filter(Users.user_id == data['user_id']).first()

        if instance_id is None:  # Post
            if chk_user is not None:
                raise ProcessingException(description="User ID is duplicated", code=413)
        else:  # Patch
            if (chk_user is not None) and (int(instance_id) != chk_user.id):
                raise ProcessingException(description="User ID is duplicated", code=413)

        data['token'] = generate_token(data['user_id'])



manager.create_api(Users
                   , url_prefix='/api/v1'
                   , collection_name='users'
                   , methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [pre_check_duplicate_userid],
                        'PATCH_SINGLE': [pre_check_duplicate_userid],
                        'GET_SINGLE': [check_token_single],
                        'GET_MANY': [check_token]
                   })


def pre_get_many_access_history(search_params=None, **kw):
    user = check_token()

    if 'filters' not in search_params:
        search_params['filters'] = []

    filt = dict(name='fk_user_id', op='eq', val=user.id)
    search_params['filters'].append(filt)


manager.create_api(AccessHistory
                   , url_prefix='/api/v1'
                   , collection_name='access_history'
                   , methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST']
                   , allow_patch_many=True
                   , preprocessors={
                        'POST': [check_token],
                        'PATCH_SINGLE': [check_token_single],
                        'GET_SINGLE': [check_token],
                        'GET_MANY': [pre_get_many_access_history]
                   })


@app.route('/api/v1/profile', methods=['GET'])
def profile_api():
    user = check_token()

    result = {'id': user.id, 'user_id': user.user_id, 'user_name': user.user_name, 'phone': user.phone,
             'user_type': user.user_type, 'email': user.email}

    return make_response(jsonify(result), 200)


@app.route('/api/v1/user_register', methods=['POST'])
def user_register_api():
    data = json.loads(request.data)
    result = ''
    print("data:",data)
    if data['user_id'] is not None:
        user = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
        if user is None:  # Insert
            new_user = Users()
            new_user.user_id = data['user_id']
            new_user.user_pw = password_encoder_512(data["user_pw"])
            new_user.user_name = data['user_name']
            new_user.user_type = data['user_type']
            new_user.user_status = 1
            new_user.email = data['email']
            db.session.add(new_user)
            db.session.commit()
            result = {'status': True, 'reason': 0, 'register_result': 1}
        else :
            result = {'status': True, 'reason': 0, 'register_result': 0}

    return make_response(jsonify(result), 200)

@app.route('/api/v1/user_modify', methods=['POST'])
def user_modify_api():
    data = json.loads(request.data)
    result = ''
    print("data:",data)
    if data['user_id'] is not None:
        user = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
        if user is not None:  # Insert
            user_pw = user.user_pw
            if data["user_pw"] != 'admin12!@':
                user_pw = password_encoder_512(data["user_pw"])
            obj = {
                "user_name":data['user_name'],
                "email":data['email'],
                "user_pw":user_pw
            }
            db.session.query(Users).filter(Users.user_id == data["user_id"]).update(obj)
            db.session.commit()
            result = {'status': True, 'reason': 0, 'register_result': 1}

    return make_response(jsonify(result), 200)



