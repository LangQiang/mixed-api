from db.db_init import *


def queryAll(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM sensitive')
    ret = cursor.fetchall()
    for ele in ret:
        print(ele)
    return ret


def insertOne(db: sqlite3.Connection, api, desc):
    print(api, desc)
    data = (api, desc)
    db.execute('INSERT OR IGNORE INTO sensitive(api, desc) VALUES (?,?)', data)
    db.commit()
