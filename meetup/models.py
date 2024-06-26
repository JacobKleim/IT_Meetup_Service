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
        return self.name if self.name else self.telegram_id


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_program = models.TextField()
    speakers = models.ManyToManyField(
        UserProfile,
        related_name='events',
        blank=True)
    organizer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='organizer_events',
        null=True
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='asked_questions')
    speaker = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='received_questions')
    text = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Question from {self.user} to {self.speaker}'


class Report(models.Model):
    speaker = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reports')
    subject = models.CharField(max_length=100)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reports')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Report from {self.speaker} on {self.event.title}'


class Donation(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_donations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_donations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Donation from {self.sender} to {self.recipient} of {self.amount} on {self.date.strftime('%Y-%m-%d %H:%M:%S')} "