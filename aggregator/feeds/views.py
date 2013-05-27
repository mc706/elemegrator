import json, ast
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext, redirect, HttpResponse
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
            feed.published = True
            elements = ast.literal_eval(json.dumps(request.POST['elements']).strip('\\r\\n'))
            print elements
            #for element in elements:
               # ast.literal_eval(element)
            feed.save()
            return redirect(reverse('view_feed', args=(feed.id,)))
    else:
        form = FeedForm()
    return render_to_response('edit.html',
        {
            'form':form,
            'title':'New Feed',
        },RequestContext(request))

@login_required
def test_feed(request):
    """Tests to see if feed will render. For pre saving purposes"""
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            #TODO: create and add elements
            feed.published = True
            for element in feed.elements.all():
                element.render
            if feed.published:
                return HttpResponse(content_type='text/plain',content="Success", status=200)
            else:
                return HttpResponse(content_type='text/plain',content="Fail", status=200)
    else:
        return HttpResponse(status=405)


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
            'title':feed.name,
        },RequestContext(request))


def sample_user_feeds(request):
    """Returns a list of feeds that the logged in user is subscribed to"""
    user = User.objects.get(pk=2)
    feeds = user.subscription.feeds.filter(published=True)
    return render_to_response('userpage.html',
        {
            'feeds':feeds,
            'title':'Sample User Feeds',
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
        
@login_required
def subscribe(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    request.user.subscription.feeds.add(feed)
    return redirect(request.META['HTTP_REFERER'])

@login_required
def unsubscribe(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    request.user.subscription.feeds.remove(feed)
    return redirect(request.META['HTTP_REFERER'])


