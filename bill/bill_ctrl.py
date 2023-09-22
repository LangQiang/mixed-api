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
        'INSERT OR REPLACE INTO BillTableTimes(bill_date, bill_table_times, bill_total, bill_opt_by,bill_shop_id, bill_pay_out) VALUES (?,?,?,?,?,?)',
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
    if totalTurnover:
        totalTurnover = round(float(totalTurnover), 1)
    else:
        totalTurnover = 0
    yesterday = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date=?', (yesterday,))
    yesterdayTurnover = cursor.fetchone()['total']
    if yesterdayTurnover:
        yesterdayTurnover = round(float(yesterdayTurnover), 1)
    else:
        yesterdayTurnover = 0

    # 上周 本周
    lastWeekStart = (datetime.now() - timedelta(days=datetime.now().weekday() + 7)).strftime('%Y-%m-%d')
    lastWeekEnd = (datetime.now() - timedelta(days=datetime.now().weekday() + 1)).strftime('%Y-%m-%d')
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (lastWeekStart, lastWeekEnd))
    lastWeekTotalTurnover = cursor.fetchone()['total']
    if lastWeekTotalTurnover:
        lastWeekTotalTurnover = round(float(lastWeekTotalTurnover), 1)
    else:
        lastWeekTotalTurnover = 0
    currentWeekStart = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
    currentWeekEnd = date.today().strftime('%Y-%m-%d')
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (currentWeekStart, currentWeekEnd))
    currentWeekTotalTurnover = cursor.fetchone()['total']
    if currentWeekTotalTurnover:
        currentWeekTotalTurnover = round(float(currentWeekTotalTurnover), 1)
    else:
        currentWeekTotalTurnover = 0

    # 上月 本月
    currentMonthStart = datetime(now.year, now.month, 1).strftime('%Y-%m-%d')
    currentMonthEnd = today
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (currentMonthStart, currentMonthEnd))
    currentMonthTotalTurnover = cursor.fetchone()['total']
    if currentMonthTotalTurnover:
        currentMonthTotalTurnover = round(float(currentMonthTotalTurnover), 1)
    else:
        currentMonthTotalTurnover = 0
    lastMonthEnd = datetime(datetime.now().year, datetime.now().month, 1) - timedelta(days=1)
    lastMonthStart = datetime(lastMonthEnd.year, lastMonthEnd.month, 1)
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes where bill_date>=? and bill_date<=?',
                        (lastMonthStart.strftime('%Y-%m-%d'), lastMonthEnd.strftime('%Y-%m-%d')))
    lastMonthTotalTurnover = cursor.fetchone()['total']
    if lastMonthTotalTurnover:
        lastMonthTotalTurnover = round(float(lastMonthTotalTurnover), 1)
    else:
        lastMonthTotalTurnover = 0

    return {'totalTurnover': totalTurnover, 'yesterdayTurnover': yesterdayTurnover,
            'lastWeekTotalTurnover': lastWeekTotalTurnover, 'currentWeekTotalTurnover': currentWeekTotalTurnover,
            'lastMonthTotalTurnover': lastMonthTotalTurnover, 'currentMonthTotalTurnover': currentMonthTotalTurnover}


def get_bill_total(db: sqlite3.Connection, shop_id):
    db.row_factory = dict_factory
    selection = '' if shop_id is None or shop_id == '' else 'where bill_shop_id=' + shop_id
    cursor = db.execute('select sum(bill_total) as total from BillTableTimes ' + selection)

    # 总共 昨日
    totalTurnover = cursor.fetchone()['total']
    return {'total': totalTurnover if totalTurnover is not None else 0}
