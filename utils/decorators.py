from flask import request
from functools import wraps
from json_response import JsonResponse
from utils.constant import ERROR
from utils.redis_utils import Redis
from utils.encrypt import generateMD5Digest
import time


def decorator_login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if token is None:
            return JsonResponse.error(error=ERROR.ACCOUNT_NOT_LOGIN)
        elif not check_token(token):
            return JsonResponse.error(error=ERROR.ACCOUNT_TOKEN_INVALID)
        else:
            return func(*args, *kwargs)

    return wrapper


def check_token(token):
    if token is None:
        return False
    cache_info = Redis.read(token)
    if cache_info:
        return True
    else:
        return False


def decorator_check_sign(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sign = request.headers.get('sign')
        timestamp = request.headers.get('timestamp')
        nonce = request.headers.get('nonce')

        if sign is None or timestamp is None or nonce is None:
            return JsonResponse.error(error=ERROR.SIGN_HEADER_FAULT)

        # 检测超时
        serverTimestamp = int(round(time.time() * 1000))
        if serverTimestamp - int(timestamp) > 30 * 1000:
            return JsonResponse.error(error=ERROR.SIGN_TIME_OUT)
        # 检测请求重放
        if Redis.exist(nonce):
            return JsonResponse.error(error=ERROR.SIGN_REQUEST_DUPLICATE)
        # 检测sign加密
        data = timestamp + '#' + nonce
        if sign != generateMD5Digest(data):
            return JsonResponse.error(error=ERROR.SIGN_VERIFY_FAILED)

        Redis.write(nonce, expire=5)

        return func(*args, *kwargs)

    return wrapper


if __name__ == '__main__':
    print(generateMD5Digest('1668764268000#1234'))
    print(generateMD5Digest('1668764268000#1234'))
    print(generateMD5Digest('1668764268000#1234'))
