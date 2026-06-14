from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'company', 'created_at')
    list_filter = ('role', 'company', 'created_at')
    search_fields = ('email', 'name')
    readonly_fields = ('created_at', 'updated_at', 'password_hash')