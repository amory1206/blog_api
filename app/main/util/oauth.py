import json
import uuid
import datetime

from flask import current_app, url_for, request, redirect, session, request ,jsonify
import flask
import requests
from app.main.model.user import User
from app.main.service.user_service import save_changes, generate_token

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def getData(self):
        pass

    def get_callback_url(self):
        return current_app.config['REDIRECT_URI']

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.url = ('https://www.facebook.com/v3.1/dialog/oauth?response_type=code&scope=email'
                '&app_id={}&redirect_uri={}').format(self.consumer_id, self.get_callback_url())

    def get_Url(self):
        return self.url

    def callback(self, auth_code):
        if auth_code is not None:
            data = {'code': auth_code,
                'client_id': self.consumer_id,
                'client_secret': self.consumer_secret,
                'scope': 'email',
                'redirect_uri': self.get_callback_url(),
                'grant_type': 'authorization_code'}
            r = requests.post('https://graph.facebook.com/oauth/access_token', data=data)
            credentials = json.loads(r.text)
            if credentials['access_token']:
                url = 'https://graph.facebook.com/me?fields=id,email&access_token={}'.format(credentials['access_token'])
                data = json.loads(requests.get(url).text)
                user = User.query.filter_by(email=data['email']).first()
                if user:
                    if user.type_user == 'google':
                        response ={
                            'message': 'User already exists. Please Log in with google'
                        }
                        return json.dumps(response)
                    else:
                        user.access_token_fb = credentials['access_token']
                        user.expires_in_fb = credentials['expires_in']
                        save_changes(user)
                        return json.dumps(generate_token(user))
                else:
                    new_user = User(
                        public_id=str(uuid.uuid4()),
                        email=data['email'],
                        registered_on=datetime.datetime.utcnow(),
                        access_token_fb = credentials['access_token'],
                        expires_in_fb= credentials['expires_in'],
                        type_user = 'fb'
                    )
                    save_changes(new_user)
                    return json.dumps(generate_token(new_user))
            return r.text
        return None
    
    def getData(self, access_token):
        url = 'https://graph.facebook.com/me?fields=id,email&access_token={}'.format(access_token)
        data = json.loads(requests.get(url).text)
        user = User.query.filter_by(email=data['email']).first()
        if user:
            if user.type_user == 'google':
                response ={
                    'message': 'User already exists. Please Log in with google'
                }
                return json.dumps(response)
            else:
                return json.dumps(generate_token(user))
        else:
            response ={
                        'message': 'User already exists. Please Log in with facebook'
                        }
            return json.dumps(response)

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.url =  ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&access_type=offline'
                '&client_id={}&redirect_uri={}&scope={}').format(self.consumer_id, self.get_callback_url(), 'https://www.googleapis.com/auth/plus.login+https://www.googleapis.com/auth/userinfo.email')

    def get_Url(self):
        return self.url

    def callback(self, auth_code):
        if auth_code is not None:
            data = {'code': auth_code,
                'client_id': self.consumer_id,
                'client_secret': self.consumer_secret,
                'scope': 'https://www.googleapis.com/auth/plus.login',
                'redirect_uri': self.get_callback_url(),
                'grant_type': 'authorization_code'}
            r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
            credentials = json.loads(r.text)
            print(r.text)
            if credentials['access_token']:
                url = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(credentials['access_token'])
                data = json.loads(requests.get(url).text)
                user = User.query.filter_by(email=data['email']).first()
                if user:
                    if user.type_user == 'fb':
                        response ={
                            'message': 'User already exists. Please Log in with facebook'
                        }
                        return json.dumps(response)
                    else:
                        user.access_token_google = credentials['access_token']
                        user.expires_in_google = credentials['expires_in']
                        save_changes(user)
                        return json.dumps(generate_token(user))
                else:
                    new_user = User(
                        public_id=str(uuid.uuid4()),
                        email=data['email'],
                        registered_on =datetime.datetime.utcnow(),
                        access_token_google = credentials['access_token'],
                        expires_in_google = credentials['expires_in'],
                        type_user = 'google'
                    )
                    save_changes(new_user)
                    return json.dumps(generate_token(new_user))
            return r.text
        return None

    def getData(self, access_token):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(access_token)
        data = json.loads(requests.get(url).text)
        user = User.query.filter_by(email=data['email']).first()
        if user:
            if user.type_user == 'fb':
                response ={
                    'message': 'User already exists. Please Log in with fb'
                }
                return json.dumps(response)
            else:
                return json.dumps(generate_token(user))
        else:
            response ={
                        'message': 'User already exists. Please Log in with google'
                        }
            return json.dumps(response)
