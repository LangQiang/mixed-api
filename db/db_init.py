import sqlite3

DATABASE = './MixedDB.db'


def connect_db():
    return sqlite3.connect(DATABASE, check_same_thread=False)


# bill_pay_out_materials TEXT,
# bill_pay_out_Labor TEXT,
# bill_pay_out_water TEXT,
# bill_pay_out_electricity TEXT,
# bill_pay_out_gas TEXT,
# bill_pay_out_dividends TEXT,
# bill_pay_out_other TEXT,

def initdb():
    # 用户表
    connect_db().execute('''CREATE TABLE if not exists User(
        user_id VARCHAR(20) NOT NULL PRIMARY KEY,
        account_name VARCHAR(20) UNIQUE,
        pass_word VARCHAR(20) NOT NULL,
        nick_name VARCHAR(20) UNIQUE,
        user_avatar TEXT,
        permission VARCHAR(20)
        )''')

    # 隐私接口 其它服务的 暂时先留着
    connect_db().execute('''CREATE TABLE if not exists sensitive(
    api VARCHAR(500) NOT NULL PRIMARY KEY,
    desc VARCHAR(500) NOT NULL
    )''')

    # 账单支付详情表
    connect_db().execute('''CREATE TABLE if not exists BillRecord(
    bill_date VARCHAR(20),
    bill_type VARCHAR(100),
    bill_amount VARCHAR(100),
    bill_shop_id INTEGER,
    primary key(bill_date, bill_type, bill_shop_id)
    )''')

    # 账单当日概览表
    connect_db().execute('''CREATE TABLE if not exists BillTableTimes(
    bill_date VARCHAR(20),
    bill_table_times VARCHAR(100),
    bill_total VARCHAR(100),
    bill_opt_by VARCHAR(100),
    bill_shop_id INTEGER,
    bill_pay_out TEXT,
    bill_bonus INTEGER,
    bill_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    primary key(bill_date, bill_shop_id)
    )''')

    # 店铺
    connect_db().execute('''CREATE TABLE if not exists Shop(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20) UNIQUE,
        img TEXT,
        desc TEXT,
        addr TEXT,
        phone VARCHAR(20),
        bill_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
        )''')

    # 天气 买不起服务 免费的自己保存
    connect_db().execute('''CREATE TABLE if not exists Weather(
            weather_date VARCHAR(20),
            weather_city VARCHAR(40),
            weather_hour VARCHAR(10),
            weather_temperature INTEGER,
            weather_temperature_day INTEGER,
            weather_temperature_night INTEGER,
            weather_condition VARCHAR(10),
            weather_win_direction VARCHAR(10),
            weather_win_speed VARCHAR(10),
            weather_air INTEGER,
            weather_humidity VARCHAR(10),
            weather_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime')),
            primary key(weather_date, weather_city, weather_hour)
            )''')

    # 采购清单列表
    connect_db().execute('''CREATE TABLE if not exists ProcureList(
                procure_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                procure_name VARCHAR(40),
                procure_desc VARCHAR(200),
                procure_notes VARCHAR(200),
                procure_state INTEGER,
                procure_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                )''')

    # 采购清单详情
    connect_db().execute('''CREATE TABLE if not exists Equipment (
                    equipment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    procure_id INTEGER,
                    equipment_name VARCHAR(40),
                    equipment_pic CHAR(100),
                    equipment_desc VARCHAR(200),
                    equipment_notes VARCHAR(200),
                    equipment_state INTEGER,
                    equipment_count INTEGER,
                    equipment_per_price INTEGER,
                    equipment_buy_channel VARCHAR(40),
                    equipment_complete_date VARCHAR(20),
                    equipment_purchaser VARCHAR(20),
                    equipment_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                    )''')

    # 资料 合同
    connect_db().execute('''CREATE TABLE if not exists Asset (
                        asset_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        asset_title VARCHAR(40),
                        asset_belong VARCHAR(40),
                        asset_format VARCHAR(20),
                        asset_url VARCHAR(200),
                        asset_extra VARCHAR(200),
                        asset_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                        )''')

    # 升级
    connect_db().execute('''CREATE TABLE if not exists Upgrade (
                            upgrade_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            upgrade_version VARCHAR(40),
                            upgrade_url VARCHAR(200),
                            upgrade_channel VARCHAR(40),
                            upgrade_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                            )''')

    # 皮肤
    connect_db().execute('''CREATE TABLE if not exists Skin (
                                skin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                skin_name VARCHAR(40) UNIQUE,
                                skin_desc VARCHAR(40),
                                skin_cover VARCHAR(200),
                                skin_effect VARCHAR(200),
                                skin_version INTEGER,
                                skin_url VARCHAR(200),
                                skin_channel VARCHAR(40),
                                skin_category VARCHAR(40),
                                skin_tag VARCHAR(40),
                                skin_type INTEGER,
                                skin_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                                )''')

    # 原材料信息
    connect_db().execute('''CREATE TABLE if not exists MaterialInfo (
                                material_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                material_name VARCHAR(40) UNIQUE,
                                material_price_per VARCHAR(40),
                                material_quantity_unit VARCHAR(40),
                                material_channel VARCHAR(40),
                                material_channel_contact_info VARCHAR(40),
                                material_type VARCHAR(40),
                                material_belong VARCHAR(40),
                                material_notes TEXT,
                                material_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                                )''')

    # 产品信息表 classify [xx-xaa-ss]表示三级
    connect_db().execute('''CREATE TABLE if not exists ProductInfo (
                                    product_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    product_name VARCHAR(40) UNIQUE,
                                    product_pic TEXT,
                                    product_type VARCHAR(40),
                                    product_classify VARCHAR(40),
                                    product_selling_price VARCHAR(40),
                                    product_notes TEXT,
                                    material_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                                    )''')

    # 产品原材料构成用量表
    connect_db().execute('''CREATE TABLE if not exists ProductComponent (
                                        product_id INTEGER,
                                        product_component_id INTEGER,
                                        product_component_name VARCHAR(40),
                                        product_component_amount INTEGER,
                                        product_component_created_time TimeStamp NOT NULL DEFAULT (DATETIME('now', 'localtime')),
                                        primary key(product_id, product_component_id)
                                        )''')

    connect_db().commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
