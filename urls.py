from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    '',

    # Landing page URL
    # (good for testing if you are on viewing the page locally or on production)
    url(r'^$', 'app.views.landing', name='landing'),

    # Static serve
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # The app
    (r'^', include('app.urls')),
)
