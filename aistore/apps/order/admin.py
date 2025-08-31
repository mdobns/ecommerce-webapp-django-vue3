from django.contrib import admin

from .models import Order,OrderItem
def order_name(obj):
    return '%s %s' %( obj.first_name, obj.last_name )
order_name.short_description = 'Name'
def set_order_shipped(modeladmin, request, queryset):
    queryset.update(status='Shipped')
set_order_shipped.short_description = "Mark as Shipped"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'status', 'paid' ,'created_at']
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInline]
    actions = [set_order_shipped]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)