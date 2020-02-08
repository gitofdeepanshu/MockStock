from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import User, Stock
from app.api import bp
from app.api.errors import bad_request, error_response
from flask_login import current_user, login_required

@bp.route('/update_user_stock', methods=['POST'])
@login_required
def update_user_stock():
    data = request.get_json() or {}
    if 'stocks' not in data:
        return bad_request('must include stocks field')
    for key, value in data['stocks'].items():
        stock = Stock.query.get(key)
        if not stock:
            return bad_request(f'Could not find stock with id={key}')
        result = current_user.add_stock(stock, quantity=value)
        if not result:
            db.sessiom.rollback()
            return bad_request(f'Could not update stock with id={key}')

    db.session.commit()
    response_data = {'money': float(current_user.money)}
    response_data['stocks'] = [{s_item.stock_id:s_item.quantity} for s_item in current_user.stock_items]

    return jsonify(response_data)
    

