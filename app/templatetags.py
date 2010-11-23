#
# Templatetags for this app, they are loaded by default in main.py
#
from google.appengine.ext.webapp import template
register = template.create_template_register()

from django.utils.safestring import mark_safe
from django.utils import simplejson

@register.filter
def json(val):
    """
    Safely converts a python value into javascript
    """
    return mark_safe(simplejson.dumps(val))
