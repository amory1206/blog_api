from flask import request, jsonify
from flask_restplus import Resource

from ..util.dto import PostDto
from ..service.post_service import save_new_post, get_all_posts, get_a_post_by_user, get_a_post_by_id
from app.main.util.decorator import token_required, infomation_required

api = PostDto.api
_post = PostDto.post
# postDetails = PostDto.postDetails

@api.route('/')
@api.header('Authorization')
class postList(Resource):
    @api.doc('list_of_posts')
    @token_required
    @infomation_required
    @api.marshal_list_with(_post, envelope='data')
    def get(self):
        """List all posts"""
        return get_all_posts()

    @api.expect(_post, validate=True)
    @api.response(201, 'post successfully created.')
    @token_required
    @infomation_required
    @api.doc('create a new post')
    def post(self):
        """Creates a new post """
        data = request.json
        return save_new_post(data=data)


@api.route('/user/<user_id>')
@api.param('user_id', 'The post identifier')
@api.response(404, 'post not found.')
@api.header('Authorization')
class post_user(Resource):
    @api.doc('get a post')
    @token_required
    @infomation_required
    @api.marshal_list_with(_post, envelope='data')
    def get(self, user_id):
        """get a post given its identifier"""
        return get_a_post_by_user(user_id)

@api.route('/<post_id>')
@api.param('post_id', 'The post identifier')
@api.response(404, 'post not found.')
@api.header('Authorization')
class post_id(Resource):
    @api.doc('get a post')
    @token_required
    @infomation_required
    @api.marshal_with(_post)
    def get(self, post_id):
        """get a post given its identifier"""
        try:
            post = get_a_post_by_id(post_id)
            if not post:
                response_object = {
                        'status': 'fail',
                        'message': 'post not found.',
                    }
                api.abort(404, response_object)
            else:
                return post
        except Exception:
            response_object = {
                        'status': 'fail',
                        'message': 'post not found.',
                    }
            api.abort(404, response_object)



