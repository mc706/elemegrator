from django.contrib import admin
from .models import Feed, Element, Subscription, Category


class SubscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subscription, SubscriptionAdmin)


class ElementInline(admin.TabularInline):
    model = Feed.elements.through

class ElementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Element, ElementAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display = ('name','get_category_display','url','published')
    inlines = [ElementInline,]
    exclude = ('elements',)

admin.site.register(Feed, FeedAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

