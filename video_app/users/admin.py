from django.contrib import admin
from .models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_staff', 'is_superuser')
    search_fields = ('username',)
