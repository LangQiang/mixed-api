from db.db_init import *
from utils.redis_utils import Redis
import json
from utils.constant import GlobalConstants


def create_shop(db: sqlite3.Connection, info):
    db.execute('INSERT OR IGNORE INTO Shop(name, img, desc,addr,phone) VALUES (?,?,?,?,?)', info)
    db.commit()


def get_shop_list(db: sqlite3.Connection, token):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM Shop')
    shop_list = cursor.fetchall()

    # 获取用户permission 字段
    permission = get_permission(db, token)
    # permission = 1152921504606846978 #测试

    # 获取用户身份
    permission_role = permission >> GlobalConstants.PERMISSION_ROLE_MASK_OFFSET

    if permission_role == GlobalConstants.PERMISSION_ROLE_STRANGER:
        print("陌生人")
        return {}
    if permission_role == GlobalConstants.PERMISSION_ROLE_SUPER_MANAGER:
        print("超级管理员")
        return shop_list

    print("正常用户")
    permission_ids = get_permission_id_list(permission)
    final_list = []
    for shop in shop_list:
        if shop['id'] in permission_ids:
            final_list.append(shop)
    return final_list


def get_permission(db, token):
    cache_info = Redis.read(token)
    user_info = json.loads(cache_info)
    userId = user_info['user_id']
    cursor = db.execute('SELECT * FROM User WHERE user_id=?', (userId,))
    ret = cursor.fetchone()
    if len(ret) == 0:
        return 0
    return int(ret['permission'])


def get_permission_id_list(permission):
    shop_list = []
    for k, v in GlobalConstants.PERMISSION_SHOP_K_V.items():
        if permission >> k & 1 == 1:
            print(v)
            shop_list.append(v)
    return shop_list


def get_shop_list_latest(db: sqlite3.Connection, shop_ids):
    db.row_factory = dict_factory
    placeholders = ','.join('?' for _ in shop_ids)
    cursor = db.execute(f'SELECT * FROM BillLatest WHERE bill_shop_id in ({placeholders})', shop_ids)
    return cursor.fetchall()
