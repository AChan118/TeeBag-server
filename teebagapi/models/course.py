from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    front_nine_par = models.IntegerField()
    back_nine_par = models.IntegerField()

    @property
    def full_name(self):
        return f'{self.name} {self.city} {self.state}'
    
    @property
    def total_par(self):
        return self.front_nine_par + self.back_nine_par