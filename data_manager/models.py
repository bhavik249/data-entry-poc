from django.db import models
from data_entry.models import BaseModel

class Events(BaseModel):
    country = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    bunting = models.BooleanField(default=False)
