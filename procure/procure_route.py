from flask import g, request, Blueprint
from .procure_ctrl import *
from json_response import JsonResponse
from utils.decorators import decorator_login_check, decorator_sign_check

procure = Blueprint('procure', __name__)


@procure.route('/procure/create', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def procure_create_route():
    name = request.json.get('procure_name')
    desc = request.json.get('procure_desc')
    notes = request.json.get('procure_notes')
    data = (name, desc, notes, 0)
    print(data)
    create_procure(g.db, data)
    return JsonResponse.success()


@procure.route('/procure/list', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def procure_list_route():
    return get_procure_list(g.db)


@procure.route('/equipment/create', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def equipment_create_route():
    data = (request.json.get('procure_id'),
            request.json.get('equipment_name'),
            request.json.get('equipment_pic'),
            request.json.get('equipment_desc'),
            request.json.get('equipment_notes'),
            request.json.get('equipment_state'),
            request.json.get('equipment_count'),
            request.json.get('equipment_per_price'),
            request.json.get('equipment_buy_channel'),
            request.json.get('equipment_complete_date'),
            request.json.get('equipment_purchaser')
            )
    create_equipment(g.db, data)
    return JsonResponse.success()


@procure.route('/equipment/update', methods=['POST'])
@decorator_sign_check
@decorator_login_check
def equipment_update_route():
    updateMap = dict()

    equipment_id = request.json.get('equipment_id')
    if equipment_id is not None:
        updateMap["equipment_id"] = equipment_id
    else:
        return JsonResponse.error("equipment_id is null")

    procure_id = request.json.get('procure_id')
    if procure_id is not None:
        updateMap["procure_id"] = procure_id
    equipment_name = request.json.get('equipment_name')
    if equipment_name is not None:
        updateMap["equipment_name"] = equipment_name
    procure_id = request.json.get('procure_id')
    if procure_id is not None:
        updateMap["procure_id"] = procure_id
    equipment_desc = request.json.get('equipment_desc')
    if equipment_desc is not None:
        updateMap["equipment_desc"] = equipment_desc
    equipment_notes = request.json.get('equipment_notes')
    if equipment_notes is not None:
        updateMap["equipment_notes"] = equipment_notes
    equipment_state = request.json.get('equipment_state')
    if equipment_state is not None:
        updateMap["equipment_state"] = equipment_state
    equipment_count = request.json.get('equipment_count')
    if equipment_count is not None:
        updateMap["equipment_count"] = equipment_count
    equipment_per_price = request.json.get('equipment_per_price')
    if equipment_per_price is not None:
        updateMap["equipment_per_price"] = equipment_per_price
    equipment_buy_channel = request.json.get('equipment_buy_channel')
    if equipment_buy_channel is not None:
        updateMap["equipment_buy_channel"] = equipment_buy_channel
    equipment_complete_date = request.json.get('equipment_complete_date')
    if equipment_complete_date is not None:
        updateMap["equipment_complete_date"] = equipment_complete_date
    equipment_purchaser = request.json.get('equipment_purchaser')
    if equipment_purchaser is not None:
        updateMap["equipment_purchaser"] = equipment_purchaser
    print(updateMap)
    update_equipment(g.db, updateMap)
    return JsonResponse.success()


@procure.route('/equipment/list/<procure_id>', methods=['GET'])
@decorator_sign_check
@decorator_login_check
def equipment_list_route(procure_id):
    return get_equipment_list(g.db, procure_id)
