from flask import g, request, Blueprint

from .bill_ctrl import *
from json_response import JsonResponse
from utils.redis_utils import Redis
from utils.decorators import decorator_login_check, decorator_sign_check
import json

bill = Blueprint('bill', __name__)


@bill.route('/bill/fetch', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def bill_fetch():
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    shop_id = request.args.get('shop_id')
    return queryBillByDate(g.db, start, end, shop_id)


@bill.route('/bill/update', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def bill_insert():
    token = request.headers.get('token')
    shop_id = request.json.get('shop_id')
    bill_date = request.json.get('date')
    bill_type_list = request.json.get('type_list')
    table_times = request.json.get('table_times')
    pay_out = request.json.get('pay_out')
    total = request.json.get('total')
    bonus = request.json.get('bonus')
    data = []
    for ele in bill_type_list:
        per_amount = float(ele.get('amount'))
        data.append((bill_date, ele.get('type'), per_amount, shop_id))
    print(data)
    opt_by = json.loads(Redis.read(token)).get('nick_name')
    insertBill(g.db, data, (bill_date, table_times, total, opt_by, shop_id, pay_out, bonus))
    return JsonResponse.success()


@bill.route('/bill/delete', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def bill_delete():
    shop_id = request.json.get('shop_id')
    bill_date = request.json.get('date')
    deleteBill(g.db, shop_id, bill_date)
    return JsonResponse.success()


@bill.route('/bill/statistics', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def bill_statistics_route():
    return get_bill_statistics(g.db)


@bill.route('/bill/total', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def bill_total_route():
    shop_id = request.args.get('bill_shop_id')
    type_name = request.args.get('type_name')
    return get_bill_total(g.db, shop_id, type_name)
