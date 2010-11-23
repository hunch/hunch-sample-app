from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson

JSON_CONTENT_TYPE = 'application/json'
JAVASCRIPT_CONTENT_TYPE = 'text/javascript'

def json_response(data):
    return HttpResponse(simplejson.dumps(data), JSON_CONTENT_TYPE)

def render_response(template, data=None, request=None):
    context_instance = RequestContext(request) if request else None
    return render_to_response(template, data, context_instance=context_instance)

def render_string(template, data=None, request=None):
    context_instance = RequestContext(request) if request else None
    return render_to_string(template, data, context_instance=context_instance)

def jsonp_response(data, callback_name):
    resp = '%s(%s)' % (callback_name, simplejson.dumps(data))
    return HttpResponse(resp, JAVASCRIPT_CONTENT_TYPE)
