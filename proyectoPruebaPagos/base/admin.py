from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Post, Veterinarian, VeterinaryClinic, 
    Shelter, Product, Pet, UserProfile, Rating, 
    Walker, Hairdresser
)

# Inlines
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class PetInline(admin.TabularInline):
    model = Pet
    extra = 1
    fields = ('name', 'shelter')

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    fields = ('veterinarian', 'score')

# Admin classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'truncated_content', 'user', 'category_list')
    list_filter = ('categories', 'user')
    search_fields = ('content', 'user__username')
    filter_horizontal = ('categories',)
    
    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Content'
    
    def category_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'clinic_count', 'average_rating')
    search_fields = ('name',)
    
    def clinic_count(self, obj):
        return obj.clinics.count()
    clinic_count.short_description = 'Number of Clinics'
    
    def average_rating(self, obj):
        ratings = Rating.objects.filter(veterinarian=obj)
        if ratings.exists():
            avg = sum(rating.score for rating in ratings) / ratings.count()
            return format_html('<span style="color: {};">{:.1f}</span>', 
                            'green' if avg >= 4 else 'orange' if avg >= 3 else 'red', 
                            avg)
        return "No ratings"
    average_rating.short_description = 'Average Rating'

@admin.register(VeterinaryClinic)
class VeterinaryClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'vet_count', 'pet_count')
    search_fields = ('name',)
    filter_horizontal = ('veterinarians',)
    
    def vet_count(self, obj):
        return obj.veterinarians.count()
    vet_count.short_description = 'Number of Veterinarians'
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Number of Pets'

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_count', 'product_count')
    search_fields = ('name',)
    inlines = [ProductInline, PetInline]
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Number of Pets'
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelter')
    list_filter = ('shelter',)
    search_fields = ('name', 'shelter__name')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelter', 'clinic_count', 'saved_count', 'adopted_count', 'liked_count')
    list_filter = ('shelter', 'veterinary_clinics')
    search_fields = ('name', 'shelter__name')
    filter_horizontal = ('veterinary_clinics',)
    
    def clinic_count(self, obj):
        return obj.veterinary_clinics.count()
    clinic_count.short_description = 'Number of Clinics'
    
    def saved_count(self, obj):
        return obj.saved_by_users.count()
    saved_count.short_description = 'Saved by Users'
    
    def adopted_count(self, obj):
        return obj.adopted_by_users.count()
    adopted_count.short_description = 'Adopted by Users'
    
    def liked_count(self, obj):
        return obj.liked_by_users.count()
    liked_count.short_description = 'Liked by Users'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'saved_pets_count', 'adopted_pets_count', 'liked_pets_count', 'rated_vets_count')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('saved_pets', 'adopted_pets', 'liked_pets')
    inlines = [RatingInline]
    
    def saved_pets_count(self, obj):
        return obj.saved_pets.count()
    saved_pets_count.short_description = 'Saved Pets'
    
    def adopted_pets_count(self, obj):
        return obj.adopted_pets.count()
    adopted_pets_count.short_description = 'Adopted Pets'
    
    def liked_pets_count(self, obj):
        return obj.liked_pets.count()
    liked_pets_count.short_description = 'Liked Pets'
    
    def rated_vets_count(self, obj):
        return obj.rated_veterinarians.count()
    rated_vets_count.short_description = 'Rated Veterinarians'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'veterinarian', 'score', 'colored_score')
    list_filter = ('score', 'veterinarian')
    search_fields = ('user_profile__user__username', 'veterinarian__name')
    
    def colored_score(self, obj):
        color = 'green' if obj.score >= 4 else 'orange' if obj.score >= 3 else 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.score)
    colored_score.short_description = 'Score'

@admin.register(Walker)
class WalkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_count')
    search_fields = ('name',)
    filter_horizontal = ('pets',)
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Number of Pets'

@admin.register(Hairdresser)
class HairdresserAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_count')
    search_fields = ('name',)
    filter_horizontal = ('pets',)
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Number of Pets'

# Custom admin site configuration
admin.site.site_header = 'Pet Services Administration'
admin.site.site_title = 'Pet Services Admin Portal'
admin.site.index_title = 'Welcome to Pet Services Admin Portal'

