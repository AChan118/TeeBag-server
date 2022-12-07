from django.db import models

class MyBag(models.Model):
    golfer = models.ForeignKey("Golfer", on_delete=models.CASCADE)
