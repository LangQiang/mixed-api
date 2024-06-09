from flask import g, request, Blueprint
from .shop_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check, decorator_sign_check


shop = Blueprint('shop', __name__)


@shop.route('/shop/create', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def shop_create_route():
    name = request.json.get('shop_name')
    img = request.json.get('shop_img')
    desc = request.json.get('shop_desc')
    addr = request.json.get('shop_addr')
    phone = request.json.get('shop_phone')
    data = (name, img, desc, addr, phone)
    print(data)
    create_shop(g.db, data)
    return JsonResponse.success()


@shop.route('/shop/list', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def shop_list_route():
    return get_shop_list(g.db, request.headers.get('token'))


@shop.route('/shop/list/latest', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def shop_list_latest_route():
    shop_ids = request.args.get('shop_ids').split(',')
    int_shop_ids = list(map(int, shop_ids))
    return get_shop_list_latest(g.db, int_shop_ids)
