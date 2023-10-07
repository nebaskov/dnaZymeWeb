from django.db import models


class MainDataBase(models.Model):
    metal_ions = models.CharField('metal_ions', max_length=50)
    kobs = models.CharField('kobs', max_length=50)
    temperature = models.CharField('temperature', max_length=50)
    ph = models.CharField('ph', max_length=50)

    def __str__(self):
        return self.metal_ions
