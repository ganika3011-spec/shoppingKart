from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account



class AccountAdmin(UserAdmin):
    list_display= ('first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links= ('first_name','last_name')
    readonly_fields= ('last_login','date_joined')
    filter_horizontal= ()
    fieldsets= () # its makes password readonly
    search_fields= ('email','username','first_name','last_name')
    list_filter= ('is_staff','is_active')
    ordering= ('-date_joined',)

# Register your models here.
admin.site.register(Account, AccountAdmin)