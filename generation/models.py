from django.db import models


class CandidatesDb(models.Model):
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
