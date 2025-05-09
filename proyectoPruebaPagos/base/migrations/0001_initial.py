# Generated by Django 5.2 on 2025-04-23 10:29

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('species', models.CharField(max_length=50)),
                ('breed', models.CharField(blank=True, max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('available', 'Available'), ('adopted', 'Adopted'), ('in_treatment', 'In Treatment')], default='available', max_length=20)),
                ('admission_date', models.DateField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='pets/')),
            ],
        ),
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('capacity', models.PositiveIntegerField()),
                ('current_occupancy', models.PositiveIntegerField(default=0)),
                ('is_accepting_animals', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Veterinarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('years_experience', models.PositiveIntegerField(default=0)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hairdresser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('rate_per_session', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_available', models.BooleanField(default=True)),
                ('specialization', models.CharField(blank=True, max_length=100)),
                ('pets', models.ManyToManyField(related_name='hairdressers', to='base.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(related_name='posts', to='base.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='base.shelter')),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='shelter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pets', to='base.shelter'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('adopted_pets', models.ManyToManyField(blank=True, related_name='adopted_by_users', to='base.pet')),
                ('liked_pets', models.ManyToManyField(blank=True, related_name='liked_by_users', to='base.pet')),
                ('saved_pets', models.ManyToManyField(blank=True, related_name='saved_by_users', to='base.pet')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(help_text='Rating from 1 to 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='base.userprofile')),
                ('veterinarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='base.veterinarian')),
            ],
            options={
                'unique_together': {('user_profile', 'veterinarian')},
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rated_veterinarians',
            field=models.ManyToManyField(related_name='rated_by_users', through='base.Rating', to='base.veterinarian'),
        ),
        migrations.CreateModel(
            name='VeterinaryClinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('opening_hours', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('veterinarians', models.ManyToManyField(related_name='clinics', to='base.veterinarian')),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='veterinary_clinics',
            field=models.ManyToManyField(related_name='pets', to='base.veterinaryclinic'),
        ),
        migrations.CreateModel(
            name='Walker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('rate_per_hour', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_available', models.BooleanField(default=True)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('pets', models.ManyToManyField(related_name='walkers', to='base.pet')),
            ],
        ),
    ]
