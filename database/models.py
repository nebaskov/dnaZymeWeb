from django.db import models

# Create your models here.


class MainDataBase(models.Model):
    name = models.CharField('name', max_length=50, default='')
    core = models.CharField('catalytic core', max_length=100, default='')
    metal_ions = models.CharField('metal_ions', max_length=50)
    kobs = models.CharField('kobs', max_length=50)
    temperature = models.CharField('temperature', max_length=50)
    ph = models.CharField('ph', max_length=50)

    class Meta:
        db_table = 'main_db'
        ordering = ['name']

    def __str__(self):
        return self.metal_ions
