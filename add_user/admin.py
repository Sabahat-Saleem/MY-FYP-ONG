from django.contrib import admin
from .models import User
from django.contrib.auth.decorators import login_required

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password')
