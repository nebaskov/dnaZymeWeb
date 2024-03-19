from django.db import models


class MainDnaDataBase(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sequence = models.CharField(max_length=96, null=False, default='')
    activity = models.FloatField(null=False, default=0)
    name = models.CharField(max_length=50, null=False, default='')
    metal_ions = models.CharField(max_length=50, null=False, default='')
    buffer = models.CharField(max_length=500, null=False, default='')
    temperature = models.FloatField(null=False, default=25)
    doi = models.CharField(max_length=100, null=False, default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'dnazyme'
        verbose_name_plural = 'dnazymes'
        db_table = 'dnazyme'

    def __str__(self):
        return self.id
