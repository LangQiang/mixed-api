from flask import g, request, Blueprint
from .skin_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check, decorator_sign_check

skin = Blueprint('skin', __name__)


@skin.route('/skin/create', methods=['POST'])
# @decorator_sign_check
# @decorator_login_check
def skin_create_route():
    skin_name = request.json.get('skin_name')
    skin_desc = request.json.get('skin_desc')
    skin_cover = request.json.get('skin_cover')
    skin_version = request.json.get('skin_version')
    skin_url = request.json.get('skin_url')
    skin_channel = request.json.get('skin_channel')
    skin_category = request.json.get('skin_category')
    skin_tag = request.json.get('skin_tag')
    skin_type = request.json.get('skin_type')
    data = (skin_name, skin_desc, skin_cover, skin_version, skin_url, skin_channel, skin_category, skin_tag, skin_type)
    print(data)
    create_skin(g.db, data)
    return JsonResponse.success()


@skin.route('/skin/list', methods=['GET'])
# @decorator_sign_check
# @decorator_login_check
def skin_list_route():
    return get_skin_list(g.db)


@skin.route('/skin/check/name/<skin_name>', methods=['GET'])
# @decorator_sign_check
# @decorator_login_check
def skin_check_name(skin_name):
    return check_skin_name(g.db, skin_name)
