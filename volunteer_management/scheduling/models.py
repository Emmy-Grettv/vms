from django.db import models
from volunteers.models import Volunteer
from events.models import Events


# Create your models here.
class Participation(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True)
    hours = models.PositiveBigIntegerField(default=0)

    def _self_(self):
        return f'{self.volunteer.name} - {self.event.name}'

