from django.db import models

# Create your models here.
class Events(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def _self_(self):
        return self.name