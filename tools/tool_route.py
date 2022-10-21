from flask import g, request, Blueprint
from .tool_ctrl import *

tool = Blueprint('tool', __name__)


@tool.route('/tool/holiday', methods=['GET'])
def holiday_route():
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    return query_holiday_state(g.db, start, end)
