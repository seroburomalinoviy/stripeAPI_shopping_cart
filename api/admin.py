from django.contrib import admin
from api.models import Item, Order, ItemInstance

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(ItemInstance)