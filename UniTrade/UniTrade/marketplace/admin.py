from django.contrib import admin

# Register your models here.

from .models import Photo, Department, Product, Productimage, Comment


class ProductAdmin(admin.ModelAdmin):
  list_display = ("product_id", "title", "seller")

admin.site.register(Department)
admin.site.register(Photo)
admin.site.register(Product, ProductAdmin)
admin.site.register(Productimage)
admin.site.register(Comment)
