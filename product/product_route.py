from flask import g, request, Blueprint
from .cost_ctrl import *
from .material_ctrl import *
from .product_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check, decorator_sign_check

product = Blueprint('product', __name__)


@product.route('/product/update', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def product_create_route():
    create_product(g.db, request.json)
    return JsonResponse.success()


@product.route('/product/delete', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def product_delete_route():
    data_opt_suc = delete_product(g.db, request.json)
    return JsonResponse.success('成功删除数据' if data_opt_suc else '不存在要删除的数据')


@product.route('/product/list', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def product_list_route():
    return get_product_list(g.db)


@product.route('/product/material/update', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def material_create_route():
    create_material(g.db, request.json)
    return JsonResponse.success()\



@product.route('/product/material/delete', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def delete_material_route():
    data_opt_suc = delete_material(g.db, request.json)
    return JsonResponse.success('成功删除数据' if data_opt_suc else '不存在要删除的数据')


@product.route('/product/material/list', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def material_list_route():
    return get_material_list(g.db)


@product.route('/product/component/update', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def cost_create_component_route():
    create_cost_component(g.db, request.json)
    return JsonResponse.success()


@product.route('/product/component/list', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def cost_component_list_route():
    return get_cost_component_list(g.db)
