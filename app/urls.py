from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',

    # Test page -- all urls that are accessible directly through the iframe
    #              need to live under this directory
    url(r'^app/$', 'app.views.test', name='test'),

    # Auth
    url(r'^authorize/$', 'app.views.authorize', name='authorize'),
    url(r'^authorized/$', 'app.views.authorized', name='authorized'),

    # Web services
    url(r'^ws/thays/$', 'app.views.ws_thays', name='ws-thays'),
)
