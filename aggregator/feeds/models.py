from django.db import models
from django.contrib.auth.models import User

from feeds.functions import get_element


class Category(models.Model):
    """Category for Feeds"""
    name = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Element(models.Model):
    """Elements on page of feed to collect"""
    type = models.CharField(max_length=8,choices=(
            ('title','Title'),
            ('body','Body'),
            ('desc','Description'),
        ))
    element = models.CharField(max_length=10)
    selector = models.TextField()
    
    def __unicode__(self):
        return self.get_type_display() + "-" + self.selector
        
    def render(self):
        import ast
        feed = self.feed_set.all()[0]
        html =  get_element(feed.url,self.element, **ast.literal_eval(self.selector))
        if not html:
            feed.published = False
            feed.save()
        return html
        
    class Meta:
        verbose_name = 'element'
        verbose_name_plural = 'elements'
    
    
class Feed(models.Model):
    """Individual web comic"""
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, blank=True, null=True)
    url = models.URLField(verbose_name="URL")
    elements = models.ManyToManyField(Element, blank=True, null=True)    
    published = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'feed'
        verbose_name_plural = 'feeds'


class Subscription(models.Model):
    """Relationship between User and their subscriptions"""
    user = models.OneToOneField(User)
    feeds = models.ManyToManyField(Feed, blank=True, null=True)
    
    def __unicode__(self):
        return self.user.get_full_name() + "'s Subscriptions"
        
    class Meta:
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"
