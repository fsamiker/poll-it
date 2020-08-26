import base64
from datetime import datetime, timedelta
import os
from backend.api import db
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    ip_addr = db.Column(db.String(45), index=True)

    option = db.relationship('Option', back_populates='votes')
    user = db.relationship('User', back_populates='votes')

    def __repr__(self):
        _voter = self.user_id
        if not _voter:
            _voter = 'Anonymous'
        return f'<{_voter} voted {self.option.body}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'option_id': self.option_id,
            'ip_addr': self.ip_addr
        }

    def from_dict(self, data):
        for field in ['ip_addr']:
            if field in data:
                setattr(self, field, data[field])


class User(PaginatedAPIMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    polls = db.relationship('Poll', backref='owner', lazy='dynamic')
    votes = db.relationship('Vote', back_populates='user')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'vote_count': len(self.votes),
            'poll_count': self.polls.count(),
            'polls': [poll.id for poll in self.polls]
        }

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class Option(PaginatedAPIMixin, db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(50))
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))

    votes = db.relationship('Vote', back_populates='option', cascade="all, delete")

    def __repr__(self):
        return f'<Option {self.body}>'

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'poll_id': self.poll_id,
            'vote_count': len(self.votes)
        }

    def from_dict(self, data):
        for field in ['body']:
            if field in data:
                setattr(self, field, data[field])

class Poll(PaginatedAPIMixin, db.Model):
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    endtime = db.Column(db.DateTime, index=True, default=lambda: datetime.utcnow()+timedelta(hours=24))
    options = db.relationship('Option', backref='poll', lazy='dynamic', cascade="all, delete")

    def __repr__(self):
        return f'<Poll {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_time': self.timestamp.isoformat()+'Z',
            'created_by': {
                'id': self.user_id,
                'username': self.owner.username
                },
            'expires_at': self.endtime.isoformat()+'Z',
            'expired': self.is_expired(),
            'options': [option.to_dict() for option in self.options],
            'chart_values': self.get_chart_data(),
            'total_votes': sum(len(option.votes) for option in self.options)
        }
    
    def get_chart_data(self):
        data = []
        labels = []
        for option in self.options:
            data.append(len(option.votes))
            labels.append(option.body)
        return {
            'data': data,
            'labels': labels
        }

    def is_expired(self):
        return datetime.utcnow() > self.endtime

    def from_dict(self, data):
        for field in ['title', 'description']:
            if field in data:
                setattr(self, field, data[field])
        if 'endtime' in data:
            setattr(self, 'endtime', datetime.fromisoformat(data['endtime']))
        for option in data['options']:
            if option['body']:
                new_option = Option()
                new_option.from_dict(option)
                self.options.append(new_option)