# Generated by Django 4.2.5 on 2023-11-03 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customar',
            name='division',
            field=models.CharField(choices=[('', 'Division Choese'), ('Dhaka', 'Dhaka'), ('Khulna', 'Khulna'), ('Rangpur', 'Rangpur'), ('Rajshahi', 'Rajshahi'), ('Barishal', 'Barishal'), ('Chattogram', 'Chattogram'), ('Mymenshing', 'Mymenshing'), ('Sylhet', 'Sylhet')], max_length=150),
        ),
    ]