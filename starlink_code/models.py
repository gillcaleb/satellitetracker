from django.db import models

# Create your models here.
class satelliteTLE(models.Model):
    name = models.CharField(max_length=128)
    L1 = models.CharField(max_length=128)
    L2 = models.CharField(max_length=128)
