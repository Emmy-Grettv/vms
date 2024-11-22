from django.db import models
from django.contrib.auth.models import User
from events.models import Event


# Create your models here.
class Profile(models.Model):
    userName = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, default=None)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    ch = [(0,'-----'), (1,'Volunteer'), (2,'Organizer')]
    userType = models.PositiveIntegerField(choices=ch, default=0)
    def __str__(self):
        return self.firstName

class Organization(models.Model):
    orgName = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    orgDivision = models.CharField(max_length=50)
    orgRating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.orgName


class Volunteer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event)
    skills = models.CharField(max_length=500)
    highLevelEducation = models.CharField(max_length=30)

    def __str__(self):
        return self.profile.userName.username

