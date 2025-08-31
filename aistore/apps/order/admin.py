from django.contrib import admin

from .models import Order,OrderItem
def order_name(obj):
    return '%s %s' %( obj.first_name, obj.last_name )
order_name.short_description = 'Name'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'created_at']
    


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)