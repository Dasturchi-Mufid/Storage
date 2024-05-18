# Generated by Django 5.0.6 on 2024-05-17 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returned',
            name='product',
        ),
        migrations.AddField(
            model_name='enter',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='returned',
            name='out',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='returned_set', to='dashboard.outlay'),
            preserve_default=False,
        ),
    ]
