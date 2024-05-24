from django.contrib import admin

from meetup.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
