"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

stories_urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^series/$', views.series_list, name='series-list'),
    url(r'^series/(?P<series>[\w-]+)/$', views.series, name='series'),
    url(
        r'^series/(?P<series>[\w-]+)/(?P<post>[\w-]+)/$',
        views.series_post, name='post'),
    url(r'^post/(?P<post>[\w-]+)/$', views.post, name='post'),
]

urlpatterns = [
    url(r'', include(stories_urlpatterns, namespace='stories')),
]
