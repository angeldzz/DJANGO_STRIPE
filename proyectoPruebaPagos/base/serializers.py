# base/serializers.py
from rest_framework import serializers
from .models import (
    Category, Post, Veterinarian, VeterinaryClinic, Shelter, 
    Product, Pet, UserProfile, Rating, Walker, Hairdresser
)
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class VeterinarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinarian
        fields = '__all__'

class VeterinaryClinicSerializer(serializers.ModelSerializer):
    veterinarians = VeterinarianSerializer(many=True, read_only=True)

    class Meta:
        model = VeterinaryClinic
        fields = '__all__'

class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    shelter = ShelterSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    shelter = ShelterSerializer(read_only=True)
    veterinary_clinics = VeterinaryClinicSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    veterinarian = VeterinarianSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

class WalkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walker
        fields = '__all__'

class HairdresserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hairdresser
        fields = '__all__'