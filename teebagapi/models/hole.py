from django.db import models

class Hole(models.Model):
    score = models.IntegerField()
    round = models.ForeignKey("Round", on_delete=models.CASCADE)