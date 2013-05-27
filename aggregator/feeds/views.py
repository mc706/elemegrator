from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext, redirect
from .models import Feed, Element, Subscription, Category
from .forms import FeedForm

def home(request):
    """Homepage"""
    if request.user.is_authenticated():
        return redirect(reverse('user_feeds'))
    recent_feeds = Feed.objects.filter(published=True).order_by('-id')[:3]
    return render_to_response('home.html',
        {
            'title':'Home',
            'recent_feeds':recent_feeds,
        }, RequestContext(request))

def feed_index(request):
    '''Returns a list of feeds'''
    feeds = Feed.objects.filter(published=True)
    return render_to_response('index.html',
        {
            'feeds':feeds,
            'title':'All Feeds',
        },RequestContext(request))
    
@login_required
def new_feed(request):
    """Create New Feed"""
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)

    else:
        pass
        #TODO: Load Feed Form
    return render_to_response('edit.html',
        {
            'title':'New Feed',
        },RequestContext(request))

@login_required
def edit_feed(request, feed_id):
    """Edit exisiting feed"""
    feed = Feed.objects.get(pk=feed_id)
    if request.method == "POST":
        pass
    else:
        pass
    return render_to_response('edit.html',
        {
            'feed':feed,
            'title':'Edit Feed',
        },RequestContext(request))

def view_feed(request, feed_id):
    """Returns individiual Feed"""    
    feed = Feed.objects.get(pk=feed_id)
    return render_to_response('detail.html',
        {
            'feed':feed,
        },RequestContext(request))

@login_required
def user_feeds(request):
    """Returns a list of feeds that the logged in user is subscribed to"""
    feeds = request.user.subscription.feeds.filter(published=True)
    return render_to_response('userpage.html',
        {
            'feeds':feeds,
            'title':'Your Feeds',
        },RequestContext(request))
    
@login_required
def user_subscriptions(request):
    feeds = Feed.objects.all()
    if request.method == "POST":
        pass
        #TODO: Update users subscriptions
    else:
        pass
        #TODO: Load subscription form
    return render_to_response('subscriptions.html',
        {
            'feeds':feeds,
            'title':'Update Subscriptions',
        },RequestContext(request))
        
        
        