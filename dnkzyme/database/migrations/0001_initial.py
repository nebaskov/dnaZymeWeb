# Generated by Django 4.2.5 on 2023-10-07 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal_ions', models.CharField(max_length=50, verbose_name='metal_ions')),
                ('kobs', models.CharField(max_length=50, verbose_name='kobs')),
                ('temperature', models.CharField(max_length=50, verbose_name='temperature')),
                ('ph', models.CharField(max_length=50, verbose_name='ph')),
            ],
        ),
    ]
