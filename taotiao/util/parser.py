

import re


def mobile(mobile_str):
    """
    校验手机号是否合法
    :return:
    """
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError(f'{mobile_str} mobile is not valid')


def code(code_str):
    """
    校验验证码是否合法
    :param code_str:
    :return:
    """
    if re.match(r'^\d{6}$', code_str):
        return code_str
    else:
        raise ValueError(f'{code_str} code is not valid')

