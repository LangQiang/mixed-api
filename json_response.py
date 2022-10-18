from utils.constant import ERROR


class JsonResponse(object):

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def custom(cls, data='', code=-1, msg='error'):
        return cls(data, code, msg)

    @classmethod
    def success(cls, data='', success: ERROR = ERROR.SUCCESS):
        return cls(data, success.code, success.msg)

    @classmethod
    def error(cls, data='', error: ERROR = ERROR.DEFAULT_ERROR):
        return cls(data, error.code, error.msg)

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
