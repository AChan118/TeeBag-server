from django.db import models

class Note(models.Model):
    text = models.CharField(max_length=100)
    date = models.DateField()
    golfer = models.ForeignKey("Golfer", on_delete=models.CASCADE)
    