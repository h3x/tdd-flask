from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import User

user_blueprint = Blueprint('users', __name__)
api = Api(user_blueprint)

user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})


class Users(Resource):

    @api.marshal_with(user)
    def get(self, user_id):
        _user = User.query.filter_by(id=user_id).first()
        if not _user:
            api.abort(404, f"User {user_id} does not exist")
        return _user, 200



class UsersList(Resource):

    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        res = {}
        _user = User.query.filter_by(email=email).first()
        if _user:
            res['message'] = 'Sorry. That email already exists.'
            return res, 400

        db.session.add(User(username=username, email=email))
        db.session.commit()

        res['message'] = f'{email} was added!'
        return res,201

    @api.marshal_with(user, as_list=True)
    def get(self):
        return User.query.all(), 200


api.add_resource(Users, '/users/<int:user_id>')
api.add_resource(UsersList, '/users')