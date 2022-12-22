from django.db import models
from .hole import Hole


class Round(models.Model):
    date = models.DateField()
    golfer = models.ForeignKey("Golfer", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    is_full_round = models.BooleanField()

@property
def course_name(self):
    return self.course.name






