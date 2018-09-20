from flask import request, Flask, redirect, url_for, render_template, flash
from flask_restplus import Resource
import json
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from app.main.util.oauth import OAuthSignIn
api = AuthDto.api
user_auth = AuthDto.user_auth
auth = AuthDto.auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)

@api.route('/authorize/<provider>')
@api.param('provider', 'The provider identifier')
class oauth_authorize(Resource):
    @api.doc('get url call back a user')
    def get(self,provider):
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.get_Url()

@api.route('/callback/<provider>')
@api.param('provider', 'The provider identifier')
class get_data(Resource):
    @api.doc('get access token a user')
    @api.expect(auth, validate=True)
    def post(self, provider):
        post_data = request.json
        auth_code = request.get_json().get('auth_code')
        oauth = OAuthSignIn.get_provider(provider)
        credentials = oauth.callback(auth_code)
        return credentials

@api.route('/getUser/<provider>')
@api.param('provider', 'The provider identifier')
class get_data(Resource):
    @api.doc('get access token a user')
    @api.expect(auth, validate=True)
    def post(self, provider):
        post_data = request.json
        auth_code = request.get_json().get('auth_code')
        oauth = OAuthSignIn.get_provider(provider)
        credentials = json.loads(oauth.getData(auth_code))
        return credentials

@api.route('/oauth2callback')
class oauth_callback(Resource):
    @api.doc('get access token a user')
    def get(self):
        code = request.args.get('code')
        return code