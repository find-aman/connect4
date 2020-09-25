from django.db import models


class MovesData(models.Model):
    key = models.CharField(max_length=50)
    move = models.CharField(max_length=10)
    column = models.CharField(max_length=1)
    player = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    winstatus = models.CharField(max_length=10 , null=True)