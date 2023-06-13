from db.db_init import *
from json_response import JsonResponse


def create_skin(db: sqlite3.Connection, info):
    db.execute(
        'INSERT OR REPLACE INTO Skin(skin_name, skin_desc, skin_cover,skin_version,skin_url, skin_channel, skin_category, skin_tag, skin_type) VALUES (?,?,?,?,?,?,?,?,?)',
        info)
    db.commit()


def get_skin_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM Skin')
    return cursor.fetchall()


def check_skin_name(db: sqlite3.Connection, skin_name):
    cursor = db.execute('SELECT * FROM Skin WHERE skin_name=?', (skin_name,))
    isExist = len(cursor.fetchall()) > 0
    return JsonResponse.success({"isExist": "true" if isExist else "false"})
