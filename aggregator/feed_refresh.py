from django.core.management import setup_environ
from aggregator import settings

setup_environ(settings)

from feeds.models import Feed

feeds = Feed.objects.filter(published=False)

for feed in feeds:
    feed.published = True
    for element in feed.elements.all():
       element.render()


