from flask import request
from flask_restplus import Resource

from ..util.dto import LikedDto
from ..service.liked_service import save_new_liked, get_a_liked_by_user, get_a_liked_by_post

api = LikedDto.api
_liked = LikedDto.liked
_liked_request = LikedDto.liked_req


@api.route('/')
@api.header('Authorization')
class likedList(Resource):
    @api.expect(_liked_request, validate=True)
    @api.response(201, 'liked successfully created.')
    @api.doc('create a new liked')
    def post(self):
        """Creates a new liked """
        data = request.json
        return save_new_liked(data=data)

@api.route('/user/<user_id>')
@api.param('user_id', 'The liked identifier')
@api.response(404, 'liked not found.')
class liked_user(Resource):
    @api.doc('get a liked')
    @api.marshal_list_with(_liked, envelope='data')
    def get(self, user_id):
        """get a liked given its identifier"""
        return get_a_liked_by_user(user_id)

@api.route('/post/<posts_id>')
@api.param('posts_id', 'The liked identifier')
@api.response(404, 'liked not found.')
class liked_post(Resource):
    @api.doc('get a liked')
    @api.marshal_list_with(_liked, envelope='data')
    def get(self, posts_id):
        """get a liked given its identifier"""
        return get_a_liked_by_post(posts_id)



