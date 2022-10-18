from enum import Enum


class ERROR(Enum):
    SUCCESS = 200, 'success'
    DEFAULT_ERROR = -1, '请求错误'

    ACCOUNT_NOT_LOGIN = 600, '用户未登录'
    ACCOUNT_TOKEN_INVALID = 601, 'token失效'
    ACCOUNT_LOGIN_ERROR_INPUT = 610, '用户名或密码错误'
    ACCOUNT_REGISTER_LIMIT = 611, '到达注册上限'
    ACCOUNT_REGISTER_NAME_DUPLICATE = 612, '用户名重复'
    ACCOUNT_REGISTER_ACCOUNT_DUPLICATE = 613, '账号重复'
    ACCOUNT_REGISTER_ERROR_PARAM = 620, '参数错误'

    SIGN_TIME_OUT = 700, '签名失效'
    SIGN_REQUEST_DUPLICATE = 701, '签名重复'
    SIGN_VERIFY_FAILED = 702, '签名校验失败'
    SIGN_HEADER_FAULT = 703, '缺少header'

    def __init__(self, code, msg):
        self._code = code
        self._msg = msg

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg


if __name__ == '__main__':
    print(ERROR.ACCOUNT_NOT_LOGIN.code)
    print(ERROR.ACCOUNT_NOT_LOGIN.msg)
