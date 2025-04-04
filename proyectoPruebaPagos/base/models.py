from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)

class VeterinaryClinic(models.Model):
    name = models.CharField(max_length=100)
    veterinarians = models.ManyToManyField(Veterinarian, related_name='clinics')

class Shelter(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='products')

class Pet(models.Model):
    name = models.CharField(max_length=100)
    shelter = models.ForeignKey(Shelter, null=True, blank=True, on_delete=models.SET_NULL, related_name='pets')
    veterinary_clinics = models.ManyToManyField(VeterinaryClinic, related_name='pets')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    saved_pets = models.ManyToManyField(Pet, related_name='saved_by_users', blank=True)
    adopted_pets = models.ManyToManyField(Pet, related_name='adopted_by_users', blank=True)
    liked_pets = models.ManyToManyField(Pet, related_name='liked_by_users', blank=True)
    rated_veterinarians = models.ManyToManyField(Veterinarian, through='Rating', related_name='rated_by_users')

class Rating(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE)
    score = models.IntegerField()

class Walker(models.Model):
    name = models.CharField(max_length=100)
    pets = models.ManyToManyField(Pet, related_name='walkers')

class Hairdresser(models.Model):
    name = models.CharField(max_length=100)
    pets = models.ManyToManyField(Pet, related_name='hairdressers')