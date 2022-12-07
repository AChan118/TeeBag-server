from django.db import models

class MyClub(models.Model):
    club = models.ForeignKey("Club", on_delete=models.CASCADE)
    my_bag = models.ForeignKey("MyBag", on_delete=models.CASCADE)
    yardage = models.IntegerField()
    brand = models.CharField(max_length=100)
    loft = models.IntegerField()
    club_note = models.CharField(max_length=100)

    @property
    def club_name(self):
        return self.club.name
    
    @property
    def club_image(self):
        return self.club.image
