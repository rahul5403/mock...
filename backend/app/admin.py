from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'phone')
    search_fields = ('email', 'username')



admin.site.site_header = "Mocklingo Admin Portal"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Mocklingo Admin"