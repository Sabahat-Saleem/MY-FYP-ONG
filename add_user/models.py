from django.db import models

class User(models.Model):
    name= models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100) 

    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created
            last_user = User.objects.order_by('-id').first()
            if last_user:
                self.id = last_user.id + 1
            else:
                self.id = 1
        super(User, self).save(*args, **kwargs)