from django.contrib import admin
from catalog.models import *
from .forms import OrderForm

admin.site.register(User)
admin.site.register(Category)
admin.site.register(ItemInOrder)


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('name', 'status', 'imageses', 'commented', 'author', 'descriptions', 'category')
    fields = ('name', 'imageses', 'status', 'descriptions', 'commented', 'category')


admin.site.register(Order, OrderAdmin)
