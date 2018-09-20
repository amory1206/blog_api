from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, save_user
from app.main.util.decorator import token_required, infomation_required

api = UserDto.api
_user = UserDto.user
update = UserDto.update


@api.route('/')
@api.header('Authorization')
class UserList(Resource):
    @token_required
    @infomation_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)
    
    @api.expect(update, validate=True)
    @api.response(201, 'User successfully update.')
    @api.doc('update a new user')
    def put(self):
        """update a new User """
        data = request.json
        return save_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
@api.header('Authorization')
class User(Resource):
    @token_required
    @infomation_required
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user



