from django.db import models
from django.contrib.auth.models import User
from food.models import Department
# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    itentity_number = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    specific_address = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='images/profiles')
    added =  models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name +" "+ self.last_name
