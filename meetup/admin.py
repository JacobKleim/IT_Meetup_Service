from django.contrib import admin

from meetup.models import UserProfile, Event, Question, Report, Donation


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    pass
