from flask import g, request, Blueprint
from json_response import JsonResponse
from .sensitive_ctrl import *

sensitive = Blueprint('sensitive', __name__)


@sensitive.route('/sensitive/fetchall', methods=["GET"])
def test_fetchall() -> str:
    return queryAll(g.db)


@sensitive.route('/sensitive/insertOne', methods=['POST'])
def test_insert_one():
    api = request.json.get('api')
    desc = request.json.get('desc')
    insertOne(g.db, api, desc)
    return JsonResponse.success()
