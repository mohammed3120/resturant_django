from django.contrib import admin
from .models import Department,Category,Meal,Ingredient,Order,Item,Invoice,InvoiceItem
# Register your models here.
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(Ingredient)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
