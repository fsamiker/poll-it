from backend.api import db
from backend.api.auth.auth import basic_auth, token_auth
from backend.api.auth import bp
from flask import jsonify


@bp.route('/tokens/', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    expiry = user.token_expiration.isoformat()+'Z'
    db.session.commit()
    return jsonify({'token': token, 'expires': expiry, 'user': user.to_dict()})


@bp.route('/tokens/', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204