from db.db_init import *


def create_shop(db: sqlite3.Connection, info):
    db.execute('INSERT OR IGNORE INTO Shop(name, img, desc,addr,phone) VALUES (?,?,?,?,?)', info)
    db.commit()


def get_shop_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM Shop')
    return cursor.fetchall()
