from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class Container (models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    def __str__(self):
        return self.name    
