import hashlib


def generateMD5Digest(data: str):
    md5Obj = hashlib.md5()
    md5Obj.update(b'857')
    md5Obj.update(data.encode("utf-8"))
    return md5Obj.hexdigest()
