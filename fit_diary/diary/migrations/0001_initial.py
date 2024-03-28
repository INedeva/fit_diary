# Generated by Django 5.0.3 on 2024-03-27 16:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DrinkEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, choices=[('Grams', 'Grams'), ('Milliliters', 'Milliliters'), ('Pieces', 'Pieces'), ('Kilograms', 'Kilograms'), ('Liters', 'Liters')], max_length=20, null=True)),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MealEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, choices=[('Grams', 'Grams'), ('Milliliters', 'Milliliters'), ('Pieces', 'Pieces'), ('Kilograms', 'Kilograms'), ('Liters', 'Liters')], max_length=20, null=True)),
                ('name', models.CharField(max_length=100)),
                ('meal_type', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], default='Breakfast', max_length=20)),
                ('calories', models.PositiveIntegerField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WaterIntakeEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, choices=[('Grams', 'Grams'), ('Milliliters', 'Milliliters'), ('Pieces', 'Pieces'), ('Kilograms', 'Kilograms'), ('Liters', 'Liters')], max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]