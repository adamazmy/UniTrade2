                    ###   AUTHOR: ZIYAD ELGYZIRI   ###



from django.contrib import admin

# Register your models here.
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_staff', 'is_active']  # Fields to display in list view
    # Other admin configuration options (search fields, filters, etc.)
