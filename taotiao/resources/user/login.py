from configparser import ConfigParser

from flask_restful import Resource
from flask import request, jsonify, current_app
from flask_restful.reqparse import RequestParser

from celery_tasks.sms.tasks import send_message
from models import User
from util.database import db_session
from datetime import datetime, timedelta

from util.jwt_util import generate_jwt
from util import parser, id_worker
from redis import Redis
from flask import request


class SendSMS(Resource):
    def get(self, mobile):
        exp_time = 5 * 60

        try:
            parser.mobile(mobile_str=mobile)
        except ValueError:
            return {'message': 'mobile is not a valid mobile'}, 404

        mobile_code = f'sms_mobile_{mobile}'
        flag_mobile = f'sms_flag_{mobile}'
        redis_conn = Redis(host='127.0.0.1', port=6379, db=0)
        flag = redis_conn.get(flag_mobile)
        if flag:
            return {'message': 'cannot be sent frequently'}, 429
        code = SendSMS.my_code()
        pl = redis_conn.pipeline()
        pl.setex(name=mobile_code, value=code, time=exp_time)
        pl.setex(name=flag_mobile, value=1, time=exp_time)
        pl.execute()
        ret = send_message.delay(mobile=mobile, code=code, time=exp_time)
        if ret:
            return {'message': 'ok', 'mobile': mobile}, 200
        return {'message': 'not ok', 'mobile': mobile}, 429

    @staticmethod
    def my_code():
        import random
        import string
        return ''.join(random.choices(string.digits, k=6))



class Login(Resource):
    def _generate_token(self, user_id, refresh=True):
        """生成token以及refresh_token"""
        payload = {
            'user_id': user_id,
            'refresh': refresh
        }
        expiry = datetime.utcnow() + \
                 timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
        print(expiry)
        token = generate_jwt(payload, expiry)

        if refresh:
            expiry = datetime.utcnow() + \
                     timedelta(days=current_app.config['JWT_REFRESH_DAYS'])
            refresh_token = generate_jwt(payload, expiry)
        else:
            refresh_token = None
        return token, refresh_token

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('mobile', required=True, location='json',
                                 type=parser.mobile)
        json_parser.add_argument('code', required=True, location='json',
                                 type=parser.code)
        args = json_parser.parse_args()  # args 是一个字典   上述参数合法的话  会存入到字典中

        mobile = args.get('mobile')
        code = args.get('code')

        mobile_code = f'sms_mobile_{mobile}'
        print(mobile_code,2222222)
        flag_mobile = f'sms_flag_{mobile}'
        redis_conn = Redis(host='127.0.0.1', port=6379, db=0)
        mobile_cod = redis_conn.get(mobile_code)
        print(mobile_cod)
        if code != mobile_cod.decode() if mobile_cod else 0:
            return {'message': 'code is invalid'}, 400

        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            user_id = id_worker.get_id()
            user = User(id=user_id, mobile=mobile, name=mobile,
                        last_login=datetime.now())
            db_session.add(user)
            db_session.commit()
        else:
            if user.status == 0:
                return {'message': 'code is invalid'}, 400

        token, refresh_token = self._generate_token(user.id)
        return {'message': 'ok', 'token': token, 'refresh_token': refresh_token}, 200



