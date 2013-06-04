from django.contrib import admin
from .models import Feed, Element, Subscription, Category

def mark_published(modeladmin, request, queryset):
    queryset.update(published=True)
mark_published.short_description = "Mark Feeds as Published"

def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
unpublish.short_description = "Mark Feeds as Unpublished"

class SubscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subscription, SubscriptionAdmin)


class ElementInline(admin.TabularInline):
    model = Feed.elements.through

class ElementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Element, ElementAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display = ('name','category','url','published')
    inlines = [ElementInline,]
    exclude = ('elements',)
    actions = [mark_published,unpublish]

admin.site.register(Feed, FeedAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

