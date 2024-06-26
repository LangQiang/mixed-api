from db.db_init import *
from json_response import JsonResponse
from utils.constant import ERROR
from utils.redis_utils import Redis
import random
import uuid
import json
from utils.logger import MyLog

def multi_nick_name(db: sqlite3.Connection, nick_name):
    cursor = db.execute('SELECT nick_name FROM User WHERE nick_name=?', (nick_name,))
    if len(cursor.fetchall()) == 0:
        return False
    else:
        return True


def multi_account(db: sqlite3.Connection, account_name):
    cursor = db.execute('SELECT account_name FROM User WHERE account_name=?', (account_name,))
    if len(cursor.fetchall()) == 0:
        return False
    else:
        return True


def generate_user_id(db: sqlite3.Connection):
    g_count = 0
    while True:
        g_count += 1
        user_id = random.randint(10000000, 99999999)
        cursor = db.execute('SELECT user_id FROM User WHERE user_id=?', (user_id,))
        if len(cursor.fetchall()) == 0:
            return user_id
        if g_count >= 10:
            break
    return -1


def generate_token():
    return str(uuid.uuid4()).replace('-', '')


def register(db: sqlite3.Connection, register_info: dict):
    account_name = register_info['account_name']
    pass_word = register_info['pass_word']
    nick_name = register_info['nick_name']

    if account_name is None \
            or pass_word is None \
            or nick_name is None \
            or len(account_name) == 0 \
            or len(pass_word) == 0 \
            or len(nick_name) == 0:
        return JsonResponse.error(error=ERROR.ACCOUNT_REGISTER_ERROR_PARAM)
    if multi_account(db, account_name):
        return JsonResponse.error(error=ERROR.ACCOUNT_REGISTER_ACCOUNT_DUPLICATE)
    if multi_nick_name(db, nick_name):
        return JsonResponse.error(error=ERROR.ACCOUNT_REGISTER_NAME_DUPLICATE)
    user_id = generate_user_id(db)
    if user_id == -1:
        return JsonResponse.error(error=ERROR.ACCOUNT_REGISTER_LIMIT)

    db.execute(
        'INSERT OR REPLACE INTO User(user_id, account_name, pass_word, nick_name, permission) VALUES (?,?,?,?)',
        (user_id, account_name, pass_word, nick_name, 0))
    db.commit()

    return JsonResponse.success()


def login(db: sqlite3.Connection, account_name, pass_word):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM User WHERE account_name=? AND pass_word=?', (account_name, pass_word))
    ret = cursor.fetchone()
    if len(ret) == 0:
        return JsonResponse.error(error=ERROR.ACCOUNT_LOGIN_ERROR_INPUT)
    print(ret)
    user_id = ret['user_id']
    account_name = ret['account_name']
    pass_word = ret['pass_word']
    nick_name = ret['nick_name']
    user_avatar = ret['user_avatar']
    permission = ret['permission']
    user_info = {'user_id': user_id, 'account_name': account_name, 'pass_word': pass_word, 'nick_name': nick_name, 'user_avatar': user_avatar, 'permission': permission}
    print(user_info)
    token = generate_token()
    Redis.write(token, json.dumps(user_info), 60 * 60 * 24 * 30)
    return JsonResponse.success({'token': token, 'nick_name': nick_name, 'user_id': user_id, 'user_avatar': user_avatar})


def account_list(db: sqlite3.Connection):
    cursor = db.execute('SELECT * FROM User')
    return cursor.fetchall()


def account_update(db: sqlite3.Connection, token, user_avatar, nick_name):
    userInfo = json.loads(Redis.read(token))
    if user_avatar is not None:
        db.execute('UPDATE User SET user_avatar=? where user_id=?', (user_avatar, userInfo.get('user_id')))
        db.commit()
        userInfo['user_avatar'] = user_avatar
    if nick_name is not None:
        MyLog.info('UPDATE UserInfo(%s): nick_name[%s -> %s]' % (userInfo.get('user_id'), userInfo['nick_name'], nick_name))
        db.execute('UPDATE User SET nick_name=? where user_id=?', (nick_name, userInfo.get('user_id')))
        db.commit()
        userInfo['nick_name'] = nick_name
    Redis.write(token, json.dumps(userInfo), 60 * 60 * 24 * 30)
    return JsonResponse.success()
