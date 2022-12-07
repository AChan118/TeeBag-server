from django.db import models

class Round(models.Model):
    date = models.DateField()
    golfer = models.ForeignKey("Golfer", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    is_full_round = models.BooleanField()
