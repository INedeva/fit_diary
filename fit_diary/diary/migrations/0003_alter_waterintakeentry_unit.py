# Generated by Django 4.2.11 on 2024-04-08 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_alter_drinkentry_options_alter_mealentry_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterintakeentry',
            name='unit',
            field=models.CharField(choices=[('Liters', 'Liters')], default='Liters', max_length=11),
        ),
    ]