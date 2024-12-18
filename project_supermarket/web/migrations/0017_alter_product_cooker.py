# Generated by Django 4.2.16 on 2024-12-16 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_alter_product_cooker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cooker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cooker', to='web.cooker'),
        ),
    ]
