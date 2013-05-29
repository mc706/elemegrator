from django.core.management import setup_environ
from aggregator import settings
import urllib2

setup_environ(settings)

from feeds.models import Feed

feeds = Feed.objects.filter(published=False)

for feed in feeds:
    feed.published = True
    feed.save()

urllib2.urlopen('http://webaggregator.net/feeds/sample/').read()


