# Generated by Django 4.2.16 on 2024-11-26 13:17

from django.db import migrations
import project_supermarket.web.managers


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_specialoffers_delete_menu_product_slug_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', project_supermarket.web.managers.SupermarketEmiUserManager()),
            ],
        ),
    ]
