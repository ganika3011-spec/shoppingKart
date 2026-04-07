from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,UserProfile
from django.utils.html import format_html



class AccountAdmin(UserAdmin):
    list_display= ('first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links= ('first_name','last_name')
    readonly_fields= ('last_login','date_joined')
    filter_horizontal= ()
    fieldsets= () # its makes password readonly
    search_fields= ('email','username','first_name','last_name')
    list_filter= ('is_staff','is_active')
    ordering= ('-date_joined',)

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html(
                "<img src='{}' width='30' height='30' style='border-radius:50%'>",
                obj.profile_picture.url
            )
        return "-"

    thumbnail.short_description = "Profile Picture"

    list_display = ("thumbnail", "user", "city", "state", "country")
# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)