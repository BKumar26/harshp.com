"""root urls for harshp
"""

from adminurls import urlpatterns as adminurlspatterns
from django.conf.urls import patterns, include, url
from django.conf import settings
import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

urlpatterns = patterns(
    '',
    # homepage and special sections
    url(
        r'^$',
        'harshp.views.home',
        name='home'
    ),
    url(
        r'^changelog/$',
        'harshp.views.changelog',
        name='changelog'
    ),
    url(
        r'^privacypolicy/$',
        'harshp.views.privacypolicy',
        name='privacypolicy'
    ),

    url(
        r'^errors/fancy404/$',
        'harshp.views.handler404',
        name='fancy404'
    ),
    url(
        r'^errors/fancy500/$',
        'harshp.views.handler500',
        name='fancy500'
    ),

    url(r'', include('sitedata.urls')),

    # apps
    url(r'', include('blog.urls')),
    url(r'', include('stories.urls')),
    url(r'', include('poems.urls')),
    url(r'', include('articles.urls')),
    url(r'', include('lifeX.urls')),
    url(r'', include('brainbank.urls')),
    url(r'', include('friends.urls')),
    url(r'', include('hobbies.urls')),
)

urlpatterns += adminurlspatterns
handler404 = 'harshp.views.handler404'
handler500 = 'harshp.views.handler500'

# if DEBUG is True it will be served automatically
if settings.DEBUG is False and settings.MODE == 'local':
    urlpatterns += patterns(
        '',
        url(
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.STATIC_ROOT
            }
        ),
    )
