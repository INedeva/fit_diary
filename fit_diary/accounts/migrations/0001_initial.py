# Generated by Django 5.0.3 on 2024-03-27 16:49

import django.db.models.deletion
import django.utils.timezone
import fit_diary.accounts.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FitDiaryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'TA user with that email already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', fit_diary.accounts.managers.FitDiaryUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='images/profile_pictures/')),
                ('facebook_profile_url', models.URLField(blank=True, null=True, unique=True)),
                ('instagram_profile_url', models.URLField(blank=True, null=True, unique=True)),
                ('linkedin_profile_url', models.URLField(blank=True, null=True, unique=True)),
                ('fitness_goals', models.CharField(blank=True, choices=[('Lose weight', 'Lose weight'), ('Gain muscle', 'Gain muscle'), ('Build endurance', 'Build endurance'), ('Improve flexibility', 'Improve flexibility'), ('Increase strength', 'Increase strength')], help_text='Your primary fitness goal', max_length=50, null=True)),
                ('goal_weight', models.DecimalField(blank=True, decimal_places=2, help_text='Goal weight in kilograms', max_digits=5, null=True)),
                ('daily_calorie_goal', models.IntegerField(blank=True, null=True)),
                ('activity_level', models.CharField(blank=True, choices=[('Sedentary', 'Sedentary'), ('Lightly Active', 'Lightly Active'), ('Moderately Active', 'Moderately Active'), ('Very Active', 'Very Active'), ('Extra Active', 'Extra Active')], max_length=50, null=True)),
                ('dietary_restrictions', models.CharField(blank=True, choices=[('None', 'None'), ('Gluten-Free', 'Gluten-Free'), ('Dairy-Free', 'Dairy-Free'), ('Nut-Free', 'Nut-Free'), ('Sugar-Free', 'Sugar-Free')], default='None', help_text='Any health restrictions', max_length=100)),
                ('preferred_diet', models.CharField(blank=True, choices=[('Balanced', 'Balanced'), ('High-Protein', 'High-Protein'), ('Low-Carb', 'Low-Carb'), ('Vegan', 'Vegan'), ('Vegetarian', 'Vegetarian'), ('Keto', 'Keto')], default='Balanced', max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]