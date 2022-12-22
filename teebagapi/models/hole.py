from django.db import models

class Hole(models.Model):
    score = models.IntegerField()
    round = models.ForeignKey("Round", on_delete=models.CASCADE)

    @property
    def round_date(self):
        return self.round.date

    @property
    def round_course(self):
        return self.round.course_name