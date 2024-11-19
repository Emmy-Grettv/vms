from django.db import models

# Create your models here.
class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    skills = models.TextField()

    def _self_(self):
        return self.name