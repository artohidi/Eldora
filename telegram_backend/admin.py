from django.contrib import admin
from .models import UserInformation


class AdminUserInformation(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'changed_username', 'changed_first_name', 'changed_last_name', 'phone_number', 'start', 'rate',
        'state')
    readonly_fields = ["user_id", "username", "first_name", "last_name", "phone_number", "start", "rate", "state"]
    ordering = ('id', 'rate')

    def changed_username(self, obj):
        if obj.username == 'ندارد':
            return obj.username
        else:
            return obj.username + "@"

    def changed_first_name(self, obj):
        if obj.first_name == '':
            obj.first_name = 'ندارد'
        return obj.first_name

    def changed_last_name(self, obj):
        if obj.last_name == '':
            obj.last_name = 'ندارد'
        return obj.last_name

    changed_username.allow_tags = True
    changed_username.short_description = 'نام کاربری انخابی'
    changed_first_name.allow_tags = True
    changed_first_name.short_description = 'نام کاربر'
    changed_last_name.allow_tags = True
    changed_last_name.short_description = 'فامیلی کاربر'


admin.site.register(UserInformation, AdminUserInformation)
