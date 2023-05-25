from db.db_init import *
from json_response import JsonResponse
from utils.constant import ERROR


def create_upgrade(db: sqlite3.Connection, info):
    db.execute(
        'INSERT OR IGNORE INTO Upgrade(upgrade_version, upgrade_url, upgrade_channel) VALUES (?,?,?)',
        info)
    db.commit()


def check_upgrade(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM Upgrade order by upgrade_version, upgrade_created_time DESC limit 1')
    ret = cursor.fetchone()
    if len(ret) == 0:
        return JsonResponse.error(error=ERROR.ACCOUNT_LOGIN_ERROR_INPUT)
    print(ret)
    upgrade_version = ret['upgrade_version']
    upgrade_url = ret['upgrade_url']
    upgrade_channel = ret['upgrade_channel']
    upgrade_info = {'upgrade_version': upgrade_version, 'upgrade_url': upgrade_url, 'upgrade_channel': upgrade_channel}
    return upgrade_info
