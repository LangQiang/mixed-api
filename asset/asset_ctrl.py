from db.db_init import *


def create_asset(db: sqlite3.Connection, info):
    db.execute(
        'INSERT OR IGNORE INTO Asset(asset_title, asset_belong, asset_format, asset_url, asset_extra) VALUES (?,?,?,?,?)',
        info)
    db.commit()


def get_asset_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM Asset')
    return cursor.fetchall()
