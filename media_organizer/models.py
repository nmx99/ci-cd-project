from django.db import models

class Format(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=200)
    formats = models.ManyToManyField(Format)

    def __str__(self):
        str = f'{self.name}'

        for format in self.formats.all():
            str += f'({format.abbreviation})'

        return str
