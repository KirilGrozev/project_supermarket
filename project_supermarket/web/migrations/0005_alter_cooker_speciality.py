# Generated by Django 4.2.16 on 2024-12-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_specialoffers_special_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooker',
            name='speciality',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
