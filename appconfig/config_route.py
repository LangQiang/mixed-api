from flask import g, request, Blueprint
from .config_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check, decorator_sign_check

config = Blueprint('config', __name__)


@config.route('/config/upgrade/create', methods=['POST'])
def asset_create_route():
    upgrade_version = request.json.get('upgrade_version')
    upgrade_url = request.json.get('upgrade_url')
    upgrade_channel = request.json.get('upgrade_channel')
    upgrade_tip = request.json.get('upgrade_tip')
    data = (upgrade_version, upgrade_url, upgrade_channel, upgrade_tip)
    print(data)
    create_upgrade(g.db, data)
    return JsonResponse.success()


@config.route('/config/upgrade/checkUpgrade', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def asset_list_route():
    return check_upgrade(g.db)
