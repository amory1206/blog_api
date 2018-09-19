from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class PostDto:
    api = Namespace('post', description='post related operations')
    post = api.model('post', {
        'id': fields.Integer(required=True, description='id of post'),
        'title': fields.String(required=True, description='title of post'),
        'description': fields.String(required=True, description='description'),
        'like_number': fields.Integer(required=True, description='like_number'),
        'user_id': fields.Integer(required=True, description='user_id'),
    })
    postDetails = api.model('post', {
        'title': fields.String(required=True, description='title of post'),
        'description': fields.String(required=True, description='description'),
        'like_number': fields.Integer(required=True, description='like_number'),
        'user_id': fields.Integer(required=True, description='user_id'),
        'content': fields.String(required=True, description='content'),
    })


class LikedDto:
    api = Namespace('liked', description='liked related operations')
    liked = api.model('liked', {
        'user_id': fields.Integer(required=True, description='user_id'),
    })
    liked_req = api.model('liked', {
        'post_id': fields.Integer(required=True, description='id of post'),
        'user_id': fields.Integer(required=True, description='user_id'),
    })
