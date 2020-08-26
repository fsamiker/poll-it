from backend.utils.validation import is_isoformat
from backend.api.auth.auth import token_auth
from backend.api import db
from backend.api.errors.error import bad_request
from backend.api.models import Option, Poll, User, Vote
from backend.api.main import bp
from flask import jsonify, request, url_for, abort


@bp.route('/users/<int:id>/', methods=['GET'])
def user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users/', methods=['GET'])
@token_auth.login_required
def get_users():
    page=request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int),100)
    data = User.to_collection_dict(User.query, page, per_page, 'main.get_users')
    return jsonify(data)

@bp.route('/users/voted/<int:id>/', methods=['GET'])
@token_auth.login_required
def get_user_voted(id):
    polls_voted = {}
    for vote in Vote.query.filter_by(user_id=id):
        poll_id = str(vote.option.poll_id)
        if poll_id in polls_voted.keys():
            polls_voted[poll_id].append(vote.option.id)
        else:
            polls_voted[poll_id] = [vote.option.id]
    return jsonify(polls_voted)

@bp.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('main.user', id=user.id)
    return response

@bp.route('/users/<int:id>/', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/polls/<int:id>/', methods=['GET'])
def poll(id):
    return jsonify(Poll.query.get_or_404(id).to_dict())

@bp.route('/polls/', methods=['GET'])
def get_polls():
    page=request.args.get('page', 1, type=int)
    user_id=request.args.get('user_id', type=int)
    if user_id:
        query = Poll.query.filter_by(user_id=user_id).order_by(Poll.timestamp.desc())
    else:
        query = Poll.query.order_by(Poll.timestamp.desc())
    per_page = min(request.args.get('per_page', 10, type=int),100)
    data = Poll.to_collection_dict(query, page, per_page, 'main.get_polls')
    return jsonify(data)

@bp.route('/polls/', methods=['POST'])
@token_auth.login_required
def create_poll():
    user = token_auth.current_user()
    data = request.get_json() or {}
    if 'title' not in data or 'options' not in data:
        return bad_request('must include title and options')
    options = data['options']
    if not isinstance(options, list) and len(options) < 2:
        return bad_request('please include at least 2 options')
    if any('body' not in option for option in options):
        return bad_request('please include option body')
    if 'endtime' in data and not is_isoformat(data['endtime']):
        return bad_request('endtime should be in isoformat')
    poll = Poll()
    poll.from_dict(data)
    user.polls.append(poll)
    db.session.add(poll)
    db.session.commit()
    response = jsonify(poll.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('main.poll', id=poll.id)
    return response

@bp.route('/polls/<int:id>/', methods=['DELETE'])
@token_auth.login_required
def delete_poll(id):
    poll = Poll.query.get_or_404(id)
    if token_auth.current_user().id != poll.user_id:
        abort(403)
    db.session.delete(poll)
    db.session.commit()
    return '', 204

@bp.route('/users/vote/', methods=['POST'])
@token_auth.login_required
def user_vote():
    user = token_auth.current_user()
    data = request.get_json() or {}
    remote_addr = request.remote_addr
    if 'option_id' not in data:
        return bad_request('vote does not have option attached')
    if user and Vote.query.filter_by(option_id=data['option_id']).filter_by(user_id=user.id).first():
        return bad_request('only one vote per user')
    option = Option.query.get_or_404(data['option_id'])
    if option.poll.is_expired():
        return bad_request('poll has expired, voting period closed')
    vote = Vote(ip_addr=remote_addr)
    vote.from_dict(data)
    if user:
        user.votes.append(vote)
    option.votes.append(vote)
    db.session.add(vote)
    db.session.commit()
    response = jsonify({'message': 'successfully submitted vote'})
    response.status_code = 201
    return response

@bp.route('/vote/', methods=['POST'])
def guest_vote():
    data = request.get_json() or {}
    remote_addr = request.remote_addr
    if 'option_id' not in data:
        return bad_request('invalid vote')
    elif Vote.query.filter_by(option_id=data['option_id']).filter_by(ip_addr=remote_addr).first():
        return bad_request('only one vote per guest')
    option = Option.query.get_or_404(data['option_id'])
    if option.poll.is_expired():
        return bad_request('poll has expired, voting period closed')
    vote = Vote(ip_addr=remote_addr)
    vote.from_dict(data)
    option.votes.append(vote)
    db.session.add(vote)
    db.session.commit()
    response = jsonify({'message': 'successfully submitted vote'})
    response.status_code = 201
    return response