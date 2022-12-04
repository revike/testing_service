from django.contrib import admin
from django.contrib.auth.models import Group

from auth_app.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_display_links = ('id', 'username', 'email', 'first_name', 'last_name')
    fields = (
        'id', 'username', 'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser', 'date_joined',)
    readonly_fields = ('id', 'date_joined',)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.site_header = 'Админ-панель Testing service'
