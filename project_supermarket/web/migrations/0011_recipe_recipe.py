# Generated by Django 4.2.16 on 2024-12-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe',
            field=models.TextField(default='l', max_length=500),
        ),
    ]
