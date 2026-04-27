from django.contrib import admin

from .models import (
    Item, OrderItem, Order, Payment, Coupon, Refund, BillingAddress, 
    Category, Slide, SiteSettings, SiteImage, Contact, Review, Promotion
)


# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['user',
                   'ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
    ]
    list_filter = ['title', 'category']
    search_fields = ['title', 'category']
    prepopulated_fields = {"slug": ("title",)}
    actions = [copy_items]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active'
    ]
    list_filter = ['title', 'is_active']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Slide)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(BillingAddress, AddressAdmin)


# Dashboard Models Admin
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_email', 'updated_at']
    
    def has_add_permission(self, request):
        # Allow only one instance
        return not SiteSettings.objects.exists()

admin.site.register(SiteSettings, SiteSettingsAdmin)


class SiteImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_type', 'is_active', 'order']
    list_filter = ['image_type', 'is_active']
    search_fields = ['title', 'image_type']

admin.site.register(SiteImage, SiteImageAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Contact, ContactAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'item', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['title', 'item__title', 'user__username']

admin.site.register(Review, ReviewAdmin)


class PromotionAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'discount_type', 'discount_value', 'is_active', 'start_date', 'end_date']
    list_filter = ['discount_type', 'is_active', 'start_date']
    search_fields = ['code', 'title']

admin.site.register(Promotion, PromotionAdmin)
