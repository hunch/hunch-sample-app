## Configuration variables

# Edit these
APP_ID = 'app_id'
APP_SECRET = 'app_secret'
APP_HOSTNAME = 'your-app.appspot.com'

# Add your auth_token here to make the test page work.
# On production, you should have your users Hunch connect
# into the app and store their auth_token
AUTH_TOKEN = ''

# Don't edit these
HOSTNAME = 'http://hunch.com'
API_HOSTNAME = 'http://api.hunch.com'
FRIENDS_API_URL = API_HOSTNAME + '/api/v1/get-friends/'
BIRTHDAYS_API_URL = API_HOSTNAME + '/api/v1/get-upcoming-birthdays/'
RECS_API_URL = API_HOSTNAME + '/api/v1/get-recommendations/'
AUTH_TOKEN_API_URL = API_HOSTNAME + '/api/v1/get-auth-token/'
CHECK_AUTH_TOKEN_API_URL = API_HOSTNAME + '/api/v1/get-token-status/'
GET_USER_INFO_API_URL = API_HOSTNAME + '/api/v1/get-user-info/'
GET_QUESTION_API_URL = API_HOSTNAME + '/api/v1/get-question/'
USER_INFO_API_URL = API_HOSTNAME + '/api/v1/get-user-info/'
THAY_API_URL = API_HOSTNAME + '/api/v1/teach-hunch-about-you/'
RESULT_API_URL = API_HOSTNAME + '/api/v1/get-results/'
PAGINATION = {
    'LIMIT': 10,
    'ON_SIDES': 2,
    'ON_ENDS': 1,
    'SIMPLE_CUTOFF': 3,
    'SHOW_END': 0,
    }
