# Generated by Django 5.0.3 on 2024-04-05 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
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
        migrations.AlterField(
            model_name='drinkentry',
            name='calories',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='drinkentry',
            name='quantity',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, message='Quantity must be at least 0.')]),
        ),
        migrations.AlterField(
            model_name='drinkentry',
            name='unit',
            field=models.CharField(blank=True, choices=[('Grams', 'Grams'), ('Milliliters', 'Milliliters'), ('Pieces', 'Pieces'), ('Kilograms', 'Kilograms'), ('Liters', 'Liters')], default='Milliliters', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='mealentry',
            name='meal_type',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], default='Breakfast', max_length=9),
        ),
        migrations.AlterField(
            model_name='mealentry',
            name='quantity',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, message='Quantity must be at least 0.')]),
        ),
        migrations.AlterField(
            model_name='mealentry',
            name='unit',
            field=models.CharField(blank=True, choices=[('Grams', 'Grams'), ('Milliliters', 'Milliliters'), ('Pieces', 'Pieces'), ('Kilograms', 'Kilograms'), ('Liters', 'Liters')], default='Grams', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='waterintakeentry',
            name='quantity',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0, message='Quantity must be at least 0.')]),
        ),
        migrations.AlterField(
            model_name='waterintakeentry',
            name='unit',
            field=models.CharField(choices=[('Liters', 'Liters')], default=0, max_length=11),
            preserve_default=False,
        ),
    ]
