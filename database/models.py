from django.db import models


class MainDnaDataBase(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False)
    sequence = models.CharField(max_length=96, null=False)
    activity = models.FloatField(null=False)
    year_of_publication = models.IntegerField(max_length=4, null=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'dnazyme'
        verbose_name_plural = 'dnazymes'
        db_table = 'dnazyme'

    def __str__(self):
        return self.name
