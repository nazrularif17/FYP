# Generated by Django 4.2.1 on 2023-06-28 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseRental', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='propStatus',
            field=models.CharField(choices=[('Available', 'Available'), ('Rented Out', 'Rented Out')], default='Available', max_length=10),
        ),
        migrations.AlterField(
            model_name='room',
            name='roomStatus',
            field=models.CharField(choices=[('Available', 'Available'), ('Rented Out', 'Rented Out')], default='Available', max_length=10),
        ),
    ]
