import sqlite3

DATABASE = './MixedDB.db'


def connect_db():
    return sqlite3.connect(DATABASE, check_same_thread=False)


def initdb():
    connect_db().execute('''CREATE TABLE if not exists User(
        user_id VARCHAR(20) NOT NULL PRIMARY KEY,
        account_name VARCHAR(20) UNIQUE,
        pass_word VARCHAR(20) NOT NULL,
        nick_name VARCHAR(20) UNIQUE,
        permission VARCHAR(20)
        )''')

    connect_db().execute('''CREATE TABLE if not exists sensitive(
    api VARCHAR(500) NOT NULL PRIMARY KEY,
    desc VARCHAR(500) NOT NULL
    )''')

    connect_db().execute('''CREATE TABLE if not exists BillRecord(
    bill_date VARCHAR(20),
    bill_type VARCHAR(100),
    bill_amount VARCHAR(100),
    bill_shop_id INTEGER,
    primary key(bill_date, bill_type, bill_shop_id)
    )''')

    connect_db().execute('''CREATE TABLE if not exists BillTableTimes(
    bill_date VARCHAR(20),
    bill_table_times VARCHAR(100),
    bill_total VARCHAR(100),
    bill_opt_by VARCHAR(100),
    bill_shop_id INTEGER,
    bill_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    primary key(bill_date, bill_shop_id)
    )''')

    connect_db().execute('''CREATE TABLE if not exists Shop(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20) UNIQUE,
        img TEXT,
        desc TEXT,
        addr TEXT,
        phone VARCHAR(20),
        bill_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
        )''')
    connect_db().commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
