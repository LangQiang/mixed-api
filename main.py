from flask import g, request

from db.db_init import *
from flask_wrapper import JsonFlask
from json_response import JsonResponse
from bill.bill_route import bill
from sensitive.sensitive_route import sensitive
from shop.shop_route import shop
from account.account_route import account
from tools.tool_route import tool
from utils.scheduler import start_weather_task
from procure.procure_route import procure
from asset.asset_route import asset
from appconfig.config_route import config
from skin.skin_route import skin
from product.product_route import product

from utils.logger import MyLog

app = JsonFlask(__name__)
app.register_blueprint(bill)
app.register_blueprint(sensitive)
app.register_blueprint(shop)
app.register_blueprint(account)
app.register_blueprint(tool)
app.register_blueprint(procure)
app.register_blueprint(asset)
app.register_blueprint(config)
app.register_blueprint(skin)
app.register_blueprint(product)


@app.before_request
def before_request():
    MyLog.log_flask_request(request, g)
    g.db = connect_db()


@app.after_request
def log_response(response):
    MyLog.log_flask_response(response, g)
    return response


@app.teardown_request
def teardown_request(exception):
    print('teardown_request:%s' % exception)
    if hasattr(g, 'db'):
        g.db.close()


@app.errorhandler(Exception)
def error_handler(e):
    e_str = str(Exception(e).args)
    MyLog.warning(request.url + e_str)
    return JsonResponse.error(e_str)


@app.route('/')
def index():
    return "welcome!!!!"


initdb()

start_weather_task()

if __name__ == '__main__':
    app.run()
