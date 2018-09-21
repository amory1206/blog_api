# blog_api
## system requirements
    -python3.6
    -pip3
    -mysql(database name blog)

### Info porject
    git clone <path git respository>
    cd blog_api
    pip3 install -r requirements.txt

    create file .env or build prod set up env follow file .env.example. sample:
    ENVIRONEMENT=dev  // env
    DB_ADDR=localhost // database address
    DB_USER_NAME=root   // user name database
    DP_PASSWORD=123456222 // password database
    DB_PORT=3306 // database port
    DB_NAME=blog /database name
    FACEBOOK_APP_ID = 'sdfa'    // facebook api id and cecret follow facebook api https://developers.facebook.com/docs
    FACEBOOK_APP_SECRET = 'fasdf'
    GOOGLE_CLIENT_ID = 'fdasfa'    // google api id and cecret follow google api https://developers.facebook.com/docs
    GOOGLE_CLIENT_SECRET = 'fdsafa'
    REDIRECT_URI=https://127.0.0.1:9999/auth/oauth2callback   link call back url rule by facebook and google


### terminal command
    python3 manage.py  db init
    python3 manage.py  db migrate
    python3 manage.py  db upgrade

    python3 manage.py run

### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    https://127.0.0.1:9999/


### Using Postman or swagger ####

    Authorization header is in the following format:

    Key: Authorization
