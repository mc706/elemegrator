import json, ast
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, RequestContext, redirect, HttpResponse
from .models import Feed, Element, Subscription, Category
from .forms import FeedForm, SubscriptionForm

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
    SESSION = {}
    SESSION['feeds'] = Feed.objects.filter(published=True)
    SESSION['title'] = 'All Feeds'
    if request.user.is_authenticated():
        SESSION['subscriptions']  = request.user.subscription.feeds.all()
    return render_to_response('index.html',SESSION,RequestContext(request))
    
@login_required
def new_feed(request):
    """Create New Feed"""
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.published = True
            feed.save()
            uinput = json.dumps(request.POST['elements']).strip('\\n').rstrip().strip('\r')
            elements = ast.literal_eval(ast.literal_eval(uinput))
            for element in elements:
                new_element = Element.objects.create(**element)
                feed.elements.add(new_element)
            feed.save()
            return redirect(reverse('view_feed', args=(feed.id,)))
    else:
        form = FeedForm()
    return render_to_response('edit.html',
        {
            'form':form,
            'title':'New Feed',
        },RequestContext(request))

@csrf_exempt
@login_required
def test_feed(request):
    """Tests to see if feed will render. For pre saving purposes"""
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.published = True
            feed.save()
            uinput = json.dumps(request.POST['elements']).strip('\\n').rstrip().strip('\r')
            elements = ast.literal_eval(ast.literal_eval(uinput))
            for element in elements:
                new_element = Element.objects.create(**element)
                feed.elements.add(new_element)
            feed.save()
            feed.published = True
            for element in feed.elements.all():
                html = element.render()
                if not html:
                    feed.published = False
            test = feed.published
            feed.delete()
            if test:
                return HttpResponse(content_type='text/plain',content="Test-Success", status=200)
            else:
                return HttpResponse(content_type='text/plain',content="Test-Fail", status=200)
        else:
            print form.errors
            return HttpResponse(status=405)
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
    SESSION = {}
    SESSION['feed'] = Feed.objects.get(pk=feed_id)
    SESSION['title'] = SESSION['feed'].name
    if request.user.is_authenticated():
        SESSION['subscriptions'] = request.user.subscription.feeds.all()
    return render_to_response('detail.html',SESSION,RequestContext(request))


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
def fast_user_feeds(request):
    """Returns a list of feeds that the logged in user is subscribed to"""
    feeds = request.user.subscription.feeds.filter(published=True)
    return render_to_response('fast_userpage.html',
        {
            'feeds':feeds,
            'title':'Your Feeds',
        },RequestContext(request))

@login_required
def load_feed(request):
    if request.method == "POST":
        try:
            feed = Feed.objects.get(pk=request.POST['feed_id'])
        except Exception as ex:
            return HttpResponse(status=404)
        html = ""
        for element in feed.elements.all():
            html += element.render()
        return HttpResponse(content_type="text/hml",content=html,status=200)
    else:
        return HttpResponse(status=403)

@login_required
def user_subscriptions(request):
    subscription = Subscription.objects.get(user=request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            try:
                form.save()
            except Exception as ex:
                print ex
        else:
            print form.errors
    else:
        form = SubscriptionForm(instance=subscription)
    return render_to_response('subscriptions.html',
        {
            'form':form,
            'title':'Update Subscriptions',
        },RequestContext(request))

@csrf_exempt
@login_required
def subscribe(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    request.user.subscription.feeds.add(feed)
    print request.user.get_full_name() + " has subscribed to " + feed.name
    return redirect(request.META['HTTP_REFERER'])

@csrf_exempt
@login_required
def unsubscribe(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    request.user.subscription.feeds.remove(feed)
    print request.user.get_full_name() + " has unsubscribed from " + feed.name
    return redirect(request.META['HTTP_REFERER'])


