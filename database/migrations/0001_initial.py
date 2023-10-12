# Generated by Django 4.2.6 on 2023-10-12 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainDnaDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('catalytic_core', models.TextField(verbose_name='catalytic_core')),
                ('buffer', models.TextField(verbose_name='buffer')),
                ('metal_ions', models.CharField(max_length=50, verbose_name='metal_ions')),
                ('kobs', models.CharField(max_length=50, verbose_name='kobs')),
                ('doi', models.CharField(max_length=50, verbose_name='doi')),
            ],
        ),
    ]
