from django.conf.urls import patterns, url


urlpatterns = patterns('feeds.views',
    url(r'new/$', 'new_feed', name='new_feed'),
    url(r'all/$', 'feed_index', name='feed_index'),
    url(r'my/$', 'user_feeds', name='user_feeds'),
    url(r'edit/(?P<feed_id>\d+)/$', 'edit_feed', name='edit_feed'),
    url(r'view/(?P<feed_id>\d+)/$', 'view_feed', name='view_feed'),
    url('^$','feed_index'),
)