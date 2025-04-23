from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Post, Veterinarian, VeterinaryClinic, Shelter, 
    Product, Pet, UserProfile, Rating, Walker, Hairdresser
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)

class CategoryInline(admin.TabularInline):
    model = Post.categories.through
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'get_category_list', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'categories')
    search_fields = ('title', 'content', 'user__username')
    date_hierarchy = 'created_at'
    inlines = [CategoryInline]
    exclude = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_category_list(self, obj):
        return obj.get_category_list()
    get_category_list.short_description = 'Categorías'

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    readonly_fields = ('created_at',)
    verbose_name = "Valoración"
    verbose_name_plural = "Valoraciones"

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'phone', 'email', 'years_experience', 'is_available', 'average_rating')
    list_filter = ('is_available', 'years_experience')
    search_fields = ('name', 'license_number', 'email')
    inlines = [RatingInline]
    
    def average_rating(self, obj):
        avg = obj.get_average_rating()
        return f"{avg:.1f}" if avg else "Sin valoraciones"
    average_rating.short_description = 'Valoración Media'

class VeterinarianInline(admin.TabularInline):
    model = VeterinaryClinic.veterinarians.through
    extra = 1
    verbose_name = "Veterinario"
    verbose_name_plural = "Veterinarios"

@admin.register(VeterinaryClinic)
class VeterinaryClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'opening_hours', 'get_vet_count', 'created_at')
    search_fields = ('name', 'address', 'email')
    list_filter = ('created_at',)
    inlines = [VeterinarianInline]
    exclude = ('veterinarians',)
    
    def get_vet_count(self, obj):
        return obj.get_vet_count()
    get_vet_count.short_description = 'Cantidad de Veterinarios'

class PetInline(admin.TabularInline):
    model = Pet
    extra = 1
    fields = ('name', 'species', 'breed', 'age', 'status')
    verbose_name = "Mascota"
    verbose_name_plural = "Mascotas"

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    verbose_name = "Producto"
    verbose_name_plural = "Productos"

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'capacity', 'current_occupancy', 
                   'available_space', 'is_full', 'is_accepting_animals')
    list_filter = ('is_accepting_animals',)
    search_fields = ('name', 'address', 'email')
    inlines = [PetInline, ProductInline]
    
    def available_space(self, obj):
        return obj.get_available_space()
    available_space.short_description = 'Espacio Disponible'
    
    def is_full(self, obj):
        return obj.is_full()
    is_full.short_description = '¿Está Lleno?'
    is_full.boolean = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelter', 'price', 'stock', 'is_in_stock', 'created_at')
    list_filter = ('shelter', 'created_at')
    search_fields = ('name', 'description', 'shelter__name')
    
    def is_in_stock(self, obj):
        return obj.is_in_stock()
    is_in_stock.short_description = 'En Stock'
    is_in_stock.boolean = True

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'shelter', 'status', 'admission_date', 'pet_image')
    list_filter = ('status', 'species', 'admission_date', 'shelter')
    search_fields = ('name', 'species', 'breed', 'description')
    date_hierarchy = 'admission_date'
    readonly_fields = ('pet_image',)
    filter_horizontal = ('veterinary_clinics',)
    
    def pet_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Sin Imagen"
    pet_image.short_description = 'Imagen'
    
    def is_adoptable(self, obj):
        return obj.is_adoptable()
    is_adoptable.short_description = '¿Adoptable?'
    is_adoptable.boolean = True

class SavedPetsInline(admin.TabularInline):
    model = UserProfile.saved_pets.through
    extra = 1
    verbose_name = "Mascota Guardada"
    verbose_name_plural = "Mascotas Guardadas"

class AdoptedPetsInline(admin.TabularInline):
    model = UserProfile.adopted_pets.through
    extra = 1
    verbose_name = "Mascota Adoptada"
    verbose_name_plural = "Mascotas Adoptadas"

class LikedPetsInline(admin.TabularInline):
    model = UserProfile.liked_pets.through
    extra = 1
    verbose_name = "Mascota Favorita"
    verbose_name_plural = "Mascotas Favoritas"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'adoption_count', 'profile_picture_preview')
    search_fields = ('user__username', 'user__email', 'phone', 'address')
    inlines = [SavedPetsInline, AdoptedPetsInline, LikedPetsInline, RatingInline]
    exclude = ('saved_pets', 'adopted_pets', 'liked_pets')
    
    def adoption_count(self, obj):
        return obj.get_adoption_count()
    adoption_count.short_description = 'Adopciones'
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" />', obj.profile_picture.url)
        return "Sin Imagen"
    profile_picture_preview.short_description = 'Foto de Perfil'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'veterinarian', 'score', 'comment', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user_profile__user__username', 'veterinarian__name', 'comment')
    date_hierarchy = 'created_at'

@admin.register(Walker)
class WalkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'rate_per_hour', 'is_available', 'experience_years', 'pet_count')
    list_filter = ('is_available', 'experience_years')
    search_fields = ('name', 'phone')
    filter_horizontal = ('pets',)
    
    def pet_count(self, obj):
        return obj.get_pet_count()
    pet_count.short_description = 'Cantidad de Mascotas'

@admin.register(Hairdresser)
class HairdresserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'rate_per_session', 'is_available', 'specialization', 'pet_count')
    list_filter = ('is_available', 'specialization')
    search_fields = ('name', 'phone', 'specialization')
    filter_horizontal = ('pets',)
    
    def pet_count(self, obj):
        return obj.get_pet_count()
    pet_count.short_description = 'Cantidad de Mascotas'