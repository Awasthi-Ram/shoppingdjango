from django.contrib import admin

# Register your models here.
from .models import Product,Contact,orders

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(orders)