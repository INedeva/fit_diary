# Generated by Django 5.0.3 on 2024-03-29 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_alter_drinkentry_quantity_alter_mealentry_quantity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drinkentry',
            options={'verbose_name_plural': 'Drink Entries'},
        ),
        migrations.AlterModelOptions(
            name='mealentry',
            options={'verbose_name_plural': 'Meal Entries'},
        ),
        migrations.AlterModelOptions(
            name='waterintakeentry',
            options={'verbose_name_plural': 'Water Intake Entries'},
        ),
    ]
