from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(models.Model):
#     name= models.CharField(max_length=70)
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100) 

#     def save(self, *args, **kwargs):
#         if not self.id:  # If the object is being created
#             last_user = User.objects.order_by('-id').first()
#             if last_user:
#                 self.id = last_user.id + 1
#             else:
#                 self.id = 1
#         super(User, self).save(*args, **kwargs)
#     def __str__(self):
#         return self.name
#************************************************
class User(AbstractUser):
    name = models.CharField(max_length=70, blank=False, null=False)  # Optional
    email = models.EmailField(unique=True)  # Ensure email is unique
    mobile_number = models.CharField(max_length=15, unique=True) # blank for temproray 


    def __str__(self):
        return self.name or "Unnamed User"
# ***********************************************************

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add additional fields based on what you want in the dashboard

    def __str__(self):
        return f"Dashboard for {self.user.username}"