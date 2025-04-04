from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    first_name= models.CharField(max_length=70, blank=False, null=False)
    last_name= models.CharField(max_length=70, blank=False, null=False)   # Optional
    email = models.EmailField(unique=True)  # Ensure email is unique
    mobile_number = models.CharField(max_length=15, unique=True) # blank for temproray 
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

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name() or "Unnamed User"

class Location(models.Model):
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=10, choices=User.TRAVEL_SEASONS)
    travel_type = models.CharField(max_length=15, choices=User.TRAVEL_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    season = models.CharField(max_length=10, choices=User.TRAVEL_SEASONS)
    travel_type = models.CharField(max_length=15, choices=User.TRAVEL_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.title

class TravelTip(models.Model):
    title = models.CharField(max_length=150)
    season = models.CharField(max_length=10, choices=User.TRAVEL_SEASONS, null=True, blank=True)
    travel_type = models.CharField(max_length=15, choices=User.TRAVEL_TYPES, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
    def full_name(self):
            return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name() or "Unnamed User"
# ***********************************************************

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add additional fields based on what you want in the dashboard

    def __str__(self):
        return f"Dashboard for {self.user.username}"
    

class Interest(models.Model):
    topic = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.topic

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)