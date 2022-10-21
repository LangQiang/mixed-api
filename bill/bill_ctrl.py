from db.db_init import *
from datetime import date, datetime, timedelta


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


def get_bill_statistics(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes')

    today = date.today().strftime('%Y-%m-%d')
    now = datetime.now()

    # 总共 昨日
    totalTurnover = cursor.fetchone()['total']
    yesterday = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    cursor = db.execute('select bill_total from BillTableTimes where bill_date=?', (yesterday,))
    yesterdayTurnover = cursor.fetchone()['bill_total']

    # 上周 本周
    lastWeekStart = (datetime.now() - timedelta(days=datetime.now().weekday() + 7)).strftime('%Y-%m-%d')
    lastWeekEnd = (datetime.now() - timedelta(days=datetime.now().weekday() + 1)).strftime('%Y-%m-%d')
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (lastWeekStart, lastWeekEnd))
    lastWeekTotalTurnover = cursor.fetchone()['total']
    currentWeekStart = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
    currentWeekEnd = date.today().strftime('%Y-%m-%d')
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (currentWeekStart, currentWeekEnd))
    currentWeekTotalTurnover = cursor.fetchone()['total']

    # 上月 本月
    currentMonthStart = datetime(now.year, now.month, 1).strftime('%Y-%m-%d')
    currentMonthEnd = today
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (currentMonthStart, currentMonthEnd))
    currentMonthTotalTurnover = cursor.fetchone()['total']

    lastMonthEnd = datetime(datetime.now().year, datetime.now().month, 1) - timedelta(days=1)
    lastMonthStart = datetime(lastMonthEnd.year, lastMonthEnd.month, 1)
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (lastMonthStart.strftime('%Y-%m-%d'), lastMonthEnd.strftime('%Y-%m-%d')))
    lastMonthTotalTurnover = cursor.fetchone()['total']

    return {'totalTurnover': round(float(totalTurnover), 1), 'yesterdayTurnover': round(float(yesterdayTurnover), 1),
            'lastWeekTotalTurnover': round(float(lastWeekTotalTurnover), 1), 'currentWeekTotalTurnover': round(float(currentWeekTotalTurnover), 1),
            'lastMonthTotalTurnover': round(float(lastMonthTotalTurnover), 1), 'currentMonthTotalTurnover': round(float(currentMonthTotalTurnover), 1)}
