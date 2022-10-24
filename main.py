from flask import g

from db.db_init import *
from flask_wrapper import JsonFlask
from json_response import JsonResponse
from bill.bill_route import bill
from sensitive.sensitive_route import sensitive
from shop.shop_route import shop
from account.account_route import account
from tools.tool_route import tool
from utils.scheduler import start_weather_task

app = JsonFlask(__name__)
app.register_blueprint(bill)
app.register_blueprint(sensitive)
app.register_blueprint(shop)
app.register_blueprint(account)
app.register_blueprint(tool)


@app.before_request
def before_request():
    print('before_request')
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    print('teardown_request:%s' % exception)
    if hasattr(g, 'db'):
        g.db.close()


@app.errorhandler(Exception)
def error_handler(e):
    return JsonResponse.error(str(Exception(e).args))


initdb()

start_weather_task()

if __name__ == '__main__':
    app.run()
