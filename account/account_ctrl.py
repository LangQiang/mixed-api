from db.db_init import *
from json_response import JsonResponse
from utils.redis_utils import Redis
import random
import uuid
import json


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
        return JsonResponse.error('参数错误', -102)
    if multi_account(db, account_name):
        return JsonResponse.error('账号重复', -103)
    if multi_nick_name(db, nick_name):
        return JsonResponse.error('用户名重复', -100)
    user_id = generate_user_id(db)
    if user_id == -1:
        return JsonResponse.error('到达注册上限', -101)

    db.execute(
        'INSERT OR REPLACE INTO User(user_id, account_name, pass_word, nick_name) VALUES (?,?,?,?)',
        (user_id, account_name, pass_word, nick_name))
    db.commit()

    return JsonResponse.success(msg='注册成功')


def login(db: sqlite3.Connection, account_name, pass_word):
    cursor = db.execute('SELECT * FROM User WHERE account_name=? AND pass_word=?', (account_name, pass_word))
    ret = cursor.fetchmany(1)
    if len(ret) == 0:
        return JsonResponse.error('用户名或密码错误', -201)
    user_id = ret[0][0]
    account_name = ret[0][1]
    pass_word = ret[0][2]
    nick_name = ret[0][3]
    user_info = {'user_id': user_id, 'account_name': account_name, 'pass_word': pass_word, 'nick_name': nick_name}
    print(user_info)
    token = generate_token()
    Redis.write(token, json.dumps(user_info), 60 * 60 * 24 * 30)
    return JsonResponse.success({'token': token, 'nick_name': nick_name, 'user_id': user_id})


def account_list(db: sqlite3.Connection):
    cursor = db.execute('SELECT * FROM User')
    return cursor.fetchall()
