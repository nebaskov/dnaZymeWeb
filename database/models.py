from django.db import models


class MainDnaDataBase(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sequence = models.CharField(max_length=96, null=False, default='')
    activity = models.FloatField(null=False, default=0)
    year_of_publication = models.IntegerField()
    name = models.CharField(max_length=50, null=False, default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'dnazyme'
        verbose_name_plural = 'dnazymes'
        db_table = 'dnazyme'

    def __str__(self):
        return self.name


class Candidates(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sequence = models.CharField(max_length=96, null=False, default='')
    activity = models.FloatField(null=False, default=0)

    class Meta:
        ordering = ['id']
        verbose_name = 'candidate'
        verbose_name_plural = 'candidates'
        db_table = 'candidates'

    def __str__(self):
        return self.sequence
