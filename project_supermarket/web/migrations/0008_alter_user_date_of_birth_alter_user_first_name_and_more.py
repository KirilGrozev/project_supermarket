# Generated by Django 4.2.16 on 2024-12-12 19:50

import django.core.validators
from django.db import migrations, models
import project_supermarket.web.validators


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2), project_supermarket.web.validators.contains_only_letters_validator]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2), project_supermarket.web.validators.contains_only_letters_validator]),
        ),
    ]