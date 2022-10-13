from flask import g, request, Blueprint
from .shop_ctrl import *
from json_response import JsonResponse

shop = Blueprint('shop', __name__)


@shop.route('/shop/create', methods=['POST'])
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
def shop_list_route():
    return get_shop_list(g.db)
