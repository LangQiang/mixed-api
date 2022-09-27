from db.db_init import *


# YY-mm-dd  range-rule:[]
def queryBillByDate(db: sqlite3.Connection, start, end, shop_id):
    real_start = '0000-00-00' if start is None else start
    real_end = '9999-99-99' if end is None else end
    print(real_start, real_end)
    db.row_factory = dict_factory

    cursor = db.execute(
        'SELECT * FROM BillTableTimes WHERE bill_date >= ? AND bill_date <= ? AND bill_shop_id == ? ORDER BY bill_date ASC',
        (real_start, real_end, shop_id))

    result = []
    for ele in cursor:
        ele_date = ele.get('bill_date')
        detail_cursor = db.execute('SELECT * FROM BillRecord WHERE bill_date == ? AND bill_shop_id == ?',
                                   (ele_date, shop_id))
        detail_data = detail_cursor.fetchall()
        ele['bill_pay_type_list'] = detail_data
        result.append(ele)
        print(ele)
    return result


def insertBill(db: sqlite3.Connection, data, table_times_data):
    for per_data in data:
        db.execute(
            'INSERT OR REPLACE INTO BillRecord(bill_date, bill_type, bill_amount, bill_shop_id) VALUES (?,?,?,?)',
            per_data)
        print(per_data)

    db.execute(
        'INSERT OR REPLACE INTO BillTableTimes(bill_date, bill_table_times, bill_total, bill_opt_by,bill_shop_id) VALUES (?,?,?,?,?)',
        table_times_data)

    db.commit()


def deleteBill(db: sqlite3.Connection, shop_id, date):
    db.execute('DELETE FROM BillRecord WHERE bill_shop_id=? AND bill_date=?', (shop_id, date))
    db.execute('DELETE FROM BillTableTimes WHERE bill_shop_id=? AND bill_date=?', (shop_id, date))
    db.commit()
