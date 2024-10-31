from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('concert', 'Concert'),
        ('workshop', 'Workshop'),
        # Add more categories as needed
    ]
    
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    capacity = models.IntegerField(default=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    bookings_count = models.IntegerField(default=0)  # Field to track bookings

    def __str__(self):
        return self.name

    def is_fully_booked(self):
        """Check if the event has reached its booking capacity."""
        return self.bookings_count >= self.capacity

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'event']  # Ensure unique booking per user-event

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
