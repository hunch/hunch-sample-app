import os
import hashlib
import urllib
import urllib2
import datetime
import random
from functools import wraps

from google.appengine.api import urlfetch, memcache
from google.appengine.ext import db
from google.appengine.runtime import DeadlineExceededError

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils import simplejson

from shortcuts import render_response, json_response

from app import config
from app.forms import ThayResponseForm
from app.models import User, ThayResponse
from app.question_ids import QUESTION_IDS
from app.utils import ajax_method, login_required, get_auth_token, make_api_request, sign_request


def landing(request):
    return render_response('landing.html', {'env': os.environ['SERVER_SOFTWARE']}, request)


def test(request):
    try:
        auth_token = get_auth_token(request) or config.AUTH_TOKEN
        if not auth_token:
            return HttpResponseRedirect(reverse('authorize') + '?' + request.GET.urlencode())
        user_id = request.GET.get('hn_user_id') if request.method == 'GET' else False
        args = {
            'auth_token': auth_token,
            'HOSTNAME': config.HOSTNAME,
            'js_cfg': {
                'user_id': user_id,
                'num_recs': 10,
                }
            }
        return render_response('app/test.html', args, request)
    except DeadlineExceededError:
        # App Engine will throw DeadlineExceededErrors from time to time
        # catch them and handle rather than returning Server Error 500
        raise Http404


def authorize(request):
    auth_token = get_auth_token(request)
    if auth_token:
        return HttpResponseRedirect(reverse('test') + '?'+ request.GET.urlencode())
    args = {'auth_url': config.HOSTNAME + '/authorize/v1?app_id=' + config.APP_ID + '&next=' + config.APP_HOSTNAME + '/test/'}
    return render_response('auth.html', args, request)


def authorized(request):
    try:
        if not request.method == 'GET':
            raise Http404
        get = request.GET
        auth_token_key = get.get('auth_token_key')

        params = {'app_id': APP_ID,
                  'auth_token_key': auth_token_key}
        params.update({'auth_sig': sign_request(params)})
        response = make_api_request(AUTH_TOKEN_API_URL, params, method="POST")
        if not response:
            raise Http404

        user_id = get.get('user_id')
        next = get.get('next')
        auth_token = response.get('auth_token')

        user = User.get_by_key_name(user_id)
        if user:
            user.auth_token = auth_token
            user.put()
        else:
            user = User(user_id=user_id, auth_token=auth_token, auth_token_key=auth_token_key, date_joined=datetime.datetime.now(), key_name=user_id)
            user.put()
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect('/test/?hn_user_id=' + user.user_id)
    except DeadlineExceededError:
        # App Engine will throw DeadlineExceededErrors from time to time
        # catch them and handle rather than returning Server Error 500
        raise Http404



@ajax_method(ThayResponseForm)
def ws_thays(request):
    cl = request.form.cleaned_data
    user = request.user
    if not user:
        raise Http404

    # store the last response
    if cl['question_id'] and cl['response_id']: #NOTE: this includes cl['response_id'] == '0'
        tr = set_thay_response(user, cl)
        params = {'auth_token': user.auth_token,
                  'question_id': cl['question_id'],
                  'response_id': cl['response_id'],
                  }
        make_api_request(config.THAY_API_URL, params)

    # get the current responses and see what can be asked next
    trs = user.thayresponse_set

    question_ids = set([tr.question_id for tr in trs])
    num_thays_answered = len([tr for tr in trs if tr.response_id != '0'])

    question_id = None
    for id in QUESTION_IDS:
        if id not in question_ids:
            question_id = id
            break

    # get the question data for the response

    if question_id:
        params = {
            'app_id': APP_ID,
            'auth_token': user.auth_token,
            'question_id': question_id,
            }
        params['auth_sig'] = sign_request(params)
        response = make_api_request(GET_QUESTION_API_URL, params)

        if not response: raise Http404('BAD RESPONSE!', response, params)

        data = response
    else:
        data = {'no_questions': True}

    data['num_thays_answered'] = num_thays_answered

    return json_response(data)
