# Generated by Django 3.1.4 on 2020-12-16 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_cupon_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.BooleanField(default=False),
        ),
    ]
