from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User, Stock
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    stocks_list = []
    purchased_list = []
    if current_user.is_authenticated:
        stocks_list = [(stock, 0) for stock in set(
            Stock.query.all()) - set(current_user.stocks)]
        purchased_list = [(stk_item.stock, stk_item.quantity)
                          for stk_item in current_user.stock_items]
    else:
        stocks_list = [(stock, 0) for stock in Stock.query.all()]

    return render_template('main/index.html', stocks=purchased_list + stocks_list)
