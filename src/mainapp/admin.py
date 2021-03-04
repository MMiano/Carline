from django.contrib import admin
from .models import Product, TransactionItem, UserProfile
# Register your models here.


class ProductAdmin(admin.ModelAdmin):

	list_display = [
		'__str__',
		'owner',
		'timestamp',
		'updated',
		'is_available',
		'is_active'

	]

	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile)
admin.site.register(TransactionItem)
