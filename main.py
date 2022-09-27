from flask import g

from db.db_init import *
from flask_wrapper import JsonFlask
from json_response import JsonResponse
from bill.bill import bill
from sensitive.sensitive import sensitive
from shop.shop import shop

app = JsonFlask(__name__)
app.register_blueprint(bill)
app.register_blueprint(sensitive)
app.register_blueprint(shop)


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
    return JsonResponse.error(msg=str(e))


initdb()

if __name__ == '__main__':
    app.run()
