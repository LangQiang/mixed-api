from db.db_init import *


def create_procure(db: sqlite3.Connection, info):
    db.execute(
        'INSERT OR IGNORE INTO ProcureList(procure_name, procure_desc, procure_notes, procure_state) VALUES (?,?,?,?)',
        info)
    db.commit()


def get_procure_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM ProcureList')
    return cursor.fetchall()


def create_equipment(db: sqlite3.Connection, info):
    db.execute(
        'INSERT OR REPLACE INTO Equipment(procure_id, equipment_name, equipment_pic, equipment_desc, equipment_notes, equipment_state, equipment_count, equipment_per_price, equipment_buy_channel, equipment_complete_date, equipment_purchaser) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
        info)
    db.commit()


def update_equipment(db: sqlite3.Connection, info_map):
    set_str = ''
    for key in info_map:
        set_str = set_str + ' \'' + key + '\'=\'' + str(info_map[key]) + '\','
    set_str = set_str[0: len(set_str) - 1]
    update_sql = 'update Equipment set ' + set_str + ' where equipment_id=' + info_map["equipment_id"]
    db.execute(update_sql)
    db.commit()


def get_equipment_list(db: sqlite3.Connection, procure_id):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM Equipment where procure_id=' + procure_id)
    return cursor.fetchall()
