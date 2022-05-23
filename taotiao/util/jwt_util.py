# -*- coding: utf-8 -*-

# Copyright (c) 2022. All rights reserved.

"""
@author: wenjie
@file: jwt_util.py
@time: 2022/5/20 10:00
@desc:

Supported platforms:

 - Linux
 - Windows

Works with Python versions 3.X.
"""

import jwt
from flask import current_app
from datetime import datetime, timedelta

# jwt  json web token
# token 认证  session认证  csrf_token认证  是依赖于浏览器的  pc端
# 如果我们想要在移动端 实现token认证  我们使用不了session认证  session认证是存储到浏览器的cookies中的
# 但是我们的移动端app是没有cookies的概念  导致不能使用session认证

# jwt是通用的token认证  可以依赖浏览器  也可以依赖移动端

# jwt实质上就是一个字符串  json字符串加base64编码生成的字符串

# jwt包含 3部分
# 1:header头部   描述jwt当前的基本算法 jwt的类型
# 2:payload载荷  jwt的签发者iss  jwt所面向的用户sub  aud是jwt接受的一方  exp过期时间 ...
# 3:signature签名密钥  将header与payload进行签名密钥算法

# jwt的通信流程

# 1.登录通过后 生成token将其返回到前端
# 2.前端获取到token值进行保存
# 3.前端携带token请求其他的接口
# 后端对传过来的token进行校验  如果正确 放行  如果不正确  抛出403或者401的状态码  需要让用户重新登录

# python的jwt本质上实现了两个方法 一个是生成jwt 一个是验证jwt


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: 载荷信息   里面可以存放自己想要的信息
    :param expiry: 过期时间
    :param secret: jwt的密钥
    :return: token
    """

    _payload = {'exp': expiry}

    _payload.update(payload)

    secret = secret if secret else current_app.config['JWT_SECRET']

    token = jwt.encode(payload=_payload, key=secret, algorithm='HS256')
    return token.decode()


def verify_jwt(token, secret=None):

    secret = secret if secret else current_app.config['JWT_SECRET']
    try:
        payload = jwt.decode(token, secret, algorithm='HS256')
    except jwt.PyJWTError:
        payload = None
    return payload


if __name__ == '__main__':
    # payload = {
    #     'user_id': 1,
    #     'username': 'wenjie'
    # }
    expiry = datetime.utcnow() + timedelta(hours=1)

    secret = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'

    # token = generate_jwt(payload, expiry, secret=secret)
    # print(token, type(token))

    # token = ''
    #
    # payload = verify_jwt(token=token, secret=secret)
    # print(payload, type(payload))

