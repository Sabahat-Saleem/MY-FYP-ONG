# from django.contrib import admin
# from .models import User
# from django.contrib.auth.decorators import login_required

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'password')

# ********************************new******************************
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('first_name', 'email', 'mobile_number','is_staff','password','is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email','mobile_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'mobile_number','is_staff', 'is_superuser')}
        ),
    )

admin.site.register(User, CustomUserAdmin)
