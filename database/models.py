from django.db import models


class MainDnaDataBase(models.Model):
    name = models.CharField('name', max_length=50)
    catalytic_core = models.TextField('catalytic_core')
    buffer = models.TextField('buffer')
    metal_ions = models.CharField('metal_ions', max_length=50)
    kobs = models.CharField('kobs', max_length=50)
    doi = models.CharField('doi', max_length=50)

    def __str__(self):
        return self.name
