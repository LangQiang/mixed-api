class JsonResponse(object):

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def success(cls, data='', code=200, msg='success'):
        return cls(data, code, msg)

    @classmethod
    def error(cls, data='', code=-1, msg='error'):
        return cls(data, code, msg)

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
