from django.contrib import admin

from meetup.models import UserProfile, Event


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventProfileAdmin(admin.ModelAdmin):
    pass
