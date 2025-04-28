from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=70, blank=False, null=False)
    last_name = models.CharField(max_length=70, blank=False, null=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    TRAVEL_SEASONS = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
    ]
    TRAVEL_TYPES = [
        ('Adventure', 'Adventure'),
        ('Relaxation', 'Relaxation'),
        ('Cultural', 'Cultural'),
        ('Wildlife', 'Wildlife'),
    ]
    preferred_season = models.CharField(max_length=10, choices=TRAVEL_SEASONS, null=True, blank=True)
    preferred_travel_type = models.CharField(max_length=15, choices=TRAVEL_TYPES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Add this field

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name() or "Unnamed User"

class Location(models.Model):
    name = models.CharField(max_length=255)
    season = models.CharField(max_length=50, choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn')])
    image = models.ImageField(upload_to='locations/')
    activities = models.TextField(default="No activities available") 

class Destination(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='locations/')
    activities = models.TextField()  # Comma-separated activities

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    season = models.CharField(max_length=50)
    travel_type = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.season})'

class TravelTip(models.Model):
    title = models.CharField(max_length=150)
    season = models.CharField(max_length=10, choices=User.TRAVEL_SEASONS, null=True, blank=True)
    travel_type = models.CharField(max_length=15, choices=User.TRAVEL_TYPES, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
# ***********************************************************

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add additional fields based on what you want in the dashboard

    def __str__(self):
        return f"Dashboard for {self.user.username}"

class InterestCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 

class Interest(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Unknown")
    description = models.TextField(default="No description available")
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    available_rooms = models.IntegerField(default=10)
    rating = models.FloatField()
    image = models.ImageField(upload_to='hotel_images/', null=True, blank=True)  # New field

    def __str__(self):
        return self.name