from django.contrib import admin

# Register your models here.
from userstuff.models import UserProfile


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'user_rating')