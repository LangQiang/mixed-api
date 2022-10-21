from flask import Blueprint, request, g
from .account_ctrl import *

account = Blueprint('account', __name__)


@account.route('/account/register', methods=['POST'])
def r_register():
    account_name = request.json.get('account_name')
    pass_word = request.json.get('pass_word')
    nick_name = request.json.get('nick_name')
    register_info = {'account_name': account_name, 'pass_word': pass_word, 'nick_name': nick_name}
    return register(g.db, register_info)


@account.route('/account/login', methods=['POST'])
def r_login():
    account_name = request.json.get('account_name')
    pass_word = request.json.get('pass_word')
    return login(g.db, account_name, pass_word)


@account.route('/account/check/<nick_name>', methods=['GET'])
def r_multi_nick_name(nick_name):
    return multi_nick_name(g.db, nick_name)


@account.route('/account/list', methods=['GET'])
def r_account_list():
    return account_list(g.db)
