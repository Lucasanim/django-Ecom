from django.contrib import admin

# Register your models here.

from .models import Item, OrderItem, Order, User, Device, Payments

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Device)
admin.site.register(Payments)
