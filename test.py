from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException
# from flask_oauth import OAuth

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth(app)

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={
                              'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)
facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email','profile_fields': 'email'}
                            )


@app.route('/')
def index_1():
    return "Hello World!"


@app.route('/test')
def index():
    return redirect(url_for('loginFacebook'))


@app.route('/loginFacebook')
def loginFacebook():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get(
                                                   'next') or request.referrer or None,
                                               _external=True))


@app.route(REDIRECT_URI_FACEBOOK)
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me?fields=name,email')
    print(me.data)
    print('Logged in as id=%s name=%s email=%s redirect=%s' % \
        (me.data['id'], me.data['name'], me.data['email'], request.args.get('next')))
    return redirect(url_for('index_1'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/login')
def index_2():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('loginGoogle'))

    access_token = access_token[0]
    from urllib.request import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except Exception as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('loginGoogle'))
        return res.read()

    return res.read()


@app.route('/loginGoogle')
def loginGoogle():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(REDIRECT_URI_GOOGLE)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index_2'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


def main():
    app.run(port=9999, ssl_context='adhoc')


if __name__ == '__main__':
    main()
