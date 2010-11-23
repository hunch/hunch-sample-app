from functools import wraps
import hashlib

from google.appengine.api import urlfetch

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils import simplejson
from django.utils.http import urlencode

from app import config
from app.models import User

## Decorators

def ajax_method(FormClass=None, method='POST', attach_user=True):
    def decorator(view_func):
        def _ajax_method(request, *args, **kwargs):
            # NOTE: uncomment the following two lines if you would like to test
            # AJAX calls in the browser (as GET requests instead of POST)
            # On production these should be activated to prevent spoofing
            if request.method != method and method != 'REQUEST': raise Http404('Request must be a ' + method)
            if not request.is_ajax(): raise Http404('Request must be AJAX')
            if FormClass:
                f = FormClass(getattr(request, method))
                if not f.is_valid(): raise Http404('Invalid form', f.errors.as_text())
                request.form = f
            if attach_user:
                request.user = get_user(request)
            return view_func(request, *args, **kwargs)
        return wraps(view_func)(_ajax_method)
    return decorator

def login_required(view_func):
    def _login_required(request, *args, **kwargs):
        auth_token = get_auth_token(request)
        if not auth_token:
            params = []
            if request.path != reverse('home'): params.extend(non_hunch_params(request))
            params.append(('next', top_url_from_request(request)))
            return HttpResponseRedirect(reverse('authorize') + '?' + urlencode(params))
        user = get_user(request)
        request.auth_token = auth_token
        request.user = user
        return view_func(request, *args, **kwargs)
    return wraps(view_func)(_login_required)

## Top Url function
def non_hunch_params(request):
    params = []
    for k,vs in request.GET.lists():
        if not k.startswith('hn_'):
            for v in vs:
                params.append((k, v))
    return params

_DEFAULT_ADD_HOST = True

def top_url_from_request(request, add_host=_DEFAULT_ADD_HOST):
    """
    Converts the current path into a top level path
    """
    return _top_url(request.path, request=request, add_host=add_host)


def top_url_from_str(app_url, add_host=_DEFAULT_ADD_HOST): #TODO(peter) - make this strip out query string arguments like the request variation does
    """
    Converts the given app url into a top level path
    """
    return _top_url(app_url, add_host=add_host)


def top_url(request, add_host=_DEFAULT_ADD_HOST):
    """
    Determines if request is a url or a request object and
    calls the appropriate top_url_FOO function.
    """
    if isinstance(request, (str, unicode)):
        app_url = request
        request = None
    else:
        app_url = request.path
    return _top_url(app_url, request=request, add_host=add_host)


## ...helper

def _top_url(app_url, request=None, add_host=_DEFAULT_ADD_HOST):
    home_url = reverse('home')

    if app_url.startswith(home_url):
        app_url = app_url[len(home_url):]

    if request and request.GET:
        params = non_hunch_params(request)
        if params: app_url += '?' + urlencode(params)

    return (config.HOSTNAME_PATH if add_host else '') + app_url #TODO(peter) - change the alan_parsons part when we update on production


## User functions
def get_auth_token(request):
    user_id = get_user_id(request)
    if not user_id:
        return False
    user = User.get_by_key_name(user_id)
    if not user or not user.auth_token:
        return False
    auth_token = user.auth_token
    params = {'app_id': config.APP_ID,
              'token': auth_token}
    params.update({'auth_sig': sign_request(params)})
    status = make_api_request(config.CHECK_AUTH_TOKEN_API_URL, params)

    if not status:
        return False
    status = status.get('status')
    if status == 'rejected':
        user.auth_token = ''
        user.auth_token_key = ''
        user.put()
        return False
    if status == 'accepted':
        return auth_token
    return False

def get_user(request):
    user_id = get_user_id(request)
    if not user_id: return None
    return User.get_by_key_name(user_id)

def get_user_id(request):
    return request.REQUEST.get('hn_user_id')

def get_topic_ids(user, blocked=False):
    user_is_male = is_male(user)
    if user_is_male == None:
        if blocked:
            return None, None
        return None
    elif user_is_male:
        # male
        if blocked:
            return config.MALE_TOPIC_IDS, config.FEMALE_TOPIC_IDS
        return config.MALE_TOPIC_IDS
    else:
        # female
        if blocked:
            return config.FEMALE_TOPIC_IDS, config.MALE_TOPIC_IDS
        return config.FEMALE_TOPIC_IDS

def is_male(user):
    response = user.thayresponse_set\
        .filter('question_id =', 'hn_424023')\
        .get()
    if not response:
        return None
        # response = make_api_request(config.AUTH_TOKEN_API_URL, params)
        # if not response:
            # # TODO(gleitz): something more intelligent that assuming you are female?
        # make_api_request()
    elif response.response_id == 'hn_1532633':
        return True
    elif response.response_id == 'hn_1532643':
        return False
    # TODO(gleitz): guess here?
    return None

def redirect_to_answer(request):
    return HttpResponseRedirect(reverse('answer') + '?' + request.GET.urlencode())


## Request functions

def make_api_request(url, params=None):
    params = params or {}
    request_url = url + '?' + urlencode(params)

    # if 'results' in request_url:
        # raise Exception(request_url)
    content = urlfetch.fetch(request_url, deadline=10)
    if content: content = content.content
    try:
        return simplejson.loads(content)
    except simplejson.JSONDecodeError, e:
        raise Exception('JSONDecodeError', url, content, e)

def sign_request(dict_object):
    encoded_args = sorted([(k.encode('utf-8') if type(k) in [str,unicode] else k, v.encode('utf-8') if type(v) in [str,unicode] else v) for k, v in dict_object.items()])
    sig = urlencode(encoded_args)
    sig += config.APP_SECRET
    return hashlib.sha1(sig).hexdigest()
