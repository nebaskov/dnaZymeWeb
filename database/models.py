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
