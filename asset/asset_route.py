from flask import g, request, Blueprint
from .asset_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check, decorator_sign_check

asset = Blueprint('asset', __name__)


@asset.route('/asset/create', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def asset_create_route():
    asset_title = request.json.get('asset_title')
    asset_belong = request.json.get('asset_belong')
    asset_format = request.json.get('asset_format')
    asset_url = request.json.get('asset_url')
    asset_extra = request.json.get('asset_extra')
    data = (asset_title, asset_belong, asset_format, asset_url, asset_extra)
    print(data)
    create_asset(g.db, data)
    return JsonResponse.success()


@asset.route('/asset/list', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def asset_list_route():
    return get_asset_list(g.db)
