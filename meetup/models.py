from django.db import models


class UserProfile(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    contact_info = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_organizer = models.BooleanField(default=False)
    is_speaker = models.BooleanField(default=False)
    state = models.CharField(max_length=30, default='START')

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_program = models.TextField()
    speakers = models.ManyToManyField(
        UserProfile,
        related_name='events',
        limit_choices_to={'is_speaker': True})

    def __str__(self):
        return self.title


class Question(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="users")
    speaker = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE)
    text = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question from {self.user} to {self.speaker}"
