from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Post(models.Model):
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    def get_category_list(self):
        return ", ".join(category.name for category in self.categories.all())

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        from django.db.models import Avg
        return Rating.objects.filter(veterinarian=self).aggregate(Avg('score'))['score__avg'] or 0

class VeterinaryClinic(models.Model):
    name = models.CharField(max_length=100)
    veterinarians = models.ManyToManyField(Veterinarian, related_name='clinics')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_vet_count(self):
        return self.veterinarians.count()

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)
    is_accepting_animals = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_available_space(self):
        return self.capacity - self.current_occupancy
    
    def is_full(self):
        return self.current_occupancy >= self.capacity

class Product(models.Model):
    name = models.CharField(max_length=100)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.shelter.name})"
    
    def is_in_stock(self):
        return self.stock > 0

class Pet(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('in_treatment', 'In Treatment'),
    )
    
    name = models.CharField(max_length=100)
    shelter = models.ForeignKey(Shelter, null=True, blank=True, on_delete=models.SET_NULL, related_name='pets')
    veterinary_clinics = models.ManyToManyField(VeterinaryClinic, related_name='pets')
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    admission_date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.species})"
    
    def is_adoptable(self):
        return self.status == 'available' and self.shelter is not None

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    saved_pets = models.ManyToManyField(Pet, related_name='saved_by_users', blank=True)
    adopted_pets = models.ManyToManyField(Pet, related_name='adopted_by_users', blank=True)
    liked_pets = models.ManyToManyField(Pet, related_name='liked_by_users', blank=True)
    rated_veterinarians = models.ManyToManyField(Veterinarian, through='Rating', related_name='rated_by_users')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def get_adoption_count(self):
        return self.adopted_pets.count()

class Rating(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings')
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user_profile', 'veterinarian')
    
    def __str__(self):
        return f"{self.user_profile.user.username}'s rating of {self.veterinarian.name}"

class Walker(models.Model):
    name = models.CharField(max_length=100)
    pets = models.ManyToManyField(Pet, related_name='walkers')
    phone = models.CharField(max_length=20)
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    experience_years = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def get_pet_count(self):
        return self.pets.count()

class Hairdresser(models.Model):
    name = models.CharField(max_length=100)
    pets = models.ManyToManyField(Pet, related_name='hairdressers')
    phone = models.CharField(max_length=20)
    rate_per_session = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    specialization = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_pet_count(self):
        return self.pets.count()
