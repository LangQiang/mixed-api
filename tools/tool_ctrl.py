from db.db_init import *


def query_holiday_state(db: sqlite3.Connection, start, end):
    real_start = '0000-00-00' if start is None else start
    real_end = '9999-99-99' if end is None else end
    db.row_factory = dict_factory

    cursor = db.execute('SELECT * FROM Holiday WHERE date >= ? AND date <= ? ORDER BY date ASC',
                        (real_start, real_end))
    return cursor.fetchall()
