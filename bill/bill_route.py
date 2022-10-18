from flask import g, request, Blueprint

from utils.constant import ERROR
from .bill_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check,decorator_check_sign

bill = Blueprint('bill', __name__)


@bill.route('/bill/fetch', methods=['GET'])
@decorator_check_sign
@decorator_login_check
def bill_fetch():
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    shop_id = request.args.get('shop_id')
    return queryBillByDate(g.db, start, end, shop_id)


@bill.route('/bill/update', methods=['POST'])
def bill_insert():
    shop_id = request.json.get('shop_id')
    date = request.json.get('date')
    opt_by = request.json.get('opt_by')
    bill_type_list = request.json.get('type_list')
    table_times = request.json.get('table_times')
    total = 0.0
    data = []
    for ele in bill_type_list:
        per_amount = float(ele.get('amount'))
        data.append((date, ele.get('type'), per_amount, shop_id))
        total += per_amount
    print("total:%s" % total)
    print(data)
    insertBill(g.db, data, (date, table_times, total, opt_by, shop_id))
    return JsonResponse.success()


@bill.route('/bill/delete', methods=['POST'])
def bill_delete():
    shop_id = request.json.get('shop_id')
    date = request.json.get('date')
    deleteBill(g.db, shop_id, date)
    return JsonResponse.success()
