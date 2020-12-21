from django.contrib import admin

# Register your models here.

from .models import Item, OrderItem, Order, User, Device, Payments, Cupon

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'ordered', 'received']

    list_display_links = [
        'user'
    ]

    list_filter = ['ordered','received']

    search_fields = ['user', 'id']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Device)
admin.site.register(Payments)
admin.site.register(Cupon)
