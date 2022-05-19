import hashlib
from datetime import timedelta, datetime


from django.utils.deprecation import MiddlewareMixin

import jwt
from jwt.exceptions import ExpiredSignatureError

EXPIRED_HOUR = 3


class UserToken(MiddlewareMixin):
    key = 'interfaceAUtomationToken'
    salt = 'interfaceAUtomation'

    @staticmethod
    def get_token(data, expired_hour=EXPIRED_HOUR):
        """用户信息转成token,并设置令牌时间"""
        new_data = dict({"exp": datetime.utcnow() + timedelta(hours=expired_hour)}, **data)
        encoded_jwt = jwt.encode(new_data, key=UserToken.key, algorithm='HS256')
        return str(encoded_jwt)

    @staticmethod
    def parse_token(token):
        """token 解析"""
        try:
            return jwt.decode(token, key=UserToken.key, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise Exception("token已过期, 请重新登录")

    @staticmethod
    def add_salt(password):
        """md5加密"""
        md5 = hashlib.md5()
        bt = f"{password}{UserToken.salt}".encode('utf-8')
        md5.update(bt)
        return md5.hexdigest()


