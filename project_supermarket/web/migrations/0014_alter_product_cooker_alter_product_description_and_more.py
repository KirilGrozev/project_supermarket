# Generated by Django 4.2.16 on 2024-12-16 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cooker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cooker', to='web.cooker'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipe',
            field=models.TextField(max_length=1000),
        ),
    ]
