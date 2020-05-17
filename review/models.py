from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length = 300)
    director = models.CharField(max_length=300)
    cast = models.CharField(max_length=500)
    description = models.TextField(max_length = 800)
    release_date = models.DateField()
    averageRating = models.FloatField(default = 0)
    image = models.URLField(default = None, null=True)

    def __str__(self):
        return self.name