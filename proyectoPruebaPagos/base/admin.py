from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from .models import (
    Category, Post, Veterinarian, VeterinaryClinic, 
    Shelter, Product, Pet, UserProfile, Rating, 
    Walker, Hairdresser
)

# Inlines
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ('name', 'price', 'stock', 'is_in_stock')
    readonly_fields = ('is_in_stock',)

class PetInline(admin.TabularInline):
    model = Pet
    extra = 1
    fields = ('name', 'shelter', 'status', 'is_adoptable')
    readonly_fields = ('is_adoptable',)

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    fields = ('veterinarian', 'score', 'comment')
    ordering = ('-created_at',)

# Admin classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'truncated_content', 'user_link', 'category_list', 'created_at', 'is_active')
    list_filter = ('categories', 'user', 'is_active', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    filter_horizontal = ('categories',)
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    
    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Content'
    
    def category_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'clinic_count', 'average_rating', 'is_available')
    search_fields = ('name', 'license_number', 'email')
    list_filter = ('is_available', 'clinics')
    list_editable = ('is_available',)
    
    def clinic_count(self, obj):
        return obj.clinics.count()
    clinic_count.short_description = 'Number of Clinics'
    
    def average_rating(self, obj):
        avg = obj.get_average_rating()
        color = 'green' if avg >= 4 else 'orange' if avg >= 3 else 'red'
        return format_html('<span style="color: {};">{:.1f}</span>', color, avg) if avg > 0 else "No ratings"
    average_rating.short_description = 'Average Rating'

@admin.register(VeterinaryClinic)
class VeterinaryClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'vet_count', 'pet_count', 'phone', 'email')
    search_fields = ('name', 'address', 'email')
    list_filter = ('created_at',)
    filter_horizontal = ('veterinarians',)
    actions = ['send_clinic_report']
    
    def vet_count(self, obj):
        return obj.veterinarians.count()
    vet_count.short_description = 'Veterinarians'
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Pets'
    
    def send_clinic_report(self, request, queryset):
        for clinic in queryset:
            # Aquí podrías implementar lógica para enviar un reporte
            messages.success(request, f"Reporte enviado para {clinic.name}")
    send_clinic_report.short_description = "Send Clinic Report"

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_count', 'product_count', 'available_space', 'is_accepting_animals')
    search_fields = ('name', 'address', 'email')
    list_filter = ('is_accepting_animals',)
    inlines = [ProductInline, PetInline]
    list_editable = ('is_accepting_animals',)
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Pets'
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'
    
    def available_space(self, obj):
        return obj.get_available_space()
    available_space.short_description = 'Available Space'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelter', 'price', 'stock', 'is_in_stock')
    list_filter = ('shelter', 'stock')
    search_fields = ('name', 'shelter__name', 'description')
    list_editable = ('price', 'stock')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelter', 'species', 'status', 'clinic_count', 'saved_count', 'adopted_count', 'liked_count')
    list_filter = ('shelter', 'status', 'veterinary_clinics', 'admission_date')
    search_fields = ('name', 'shelter__name', 'species', 'breed')
    filter_horizontal = ('veterinary_clinics',)
    list_editable = ('status',)
    date_hierarchy = 'admission_date'
    actions = ['mark_as_adopted']
    
    def clinic_count(self, obj):
        return obj.veterinary_clinics.count()
    clinic_count.short_description = 'Clinics'
    
    def saved_count(self, obj):
        return obj.saved_by_users.count()
    saved_count.short_description = 'Saved'
    
    def adopted_count(self, obj):
        return obj.adopted_by_users.count()
    adopted_count.short_description = 'Adopted'
    
    def liked_count(self, obj):
        return obj.liked_by_users.count()
    liked_count.short_description = 'Liked'
    
    def mark_as_adopted(self, request, queryset):
        queryset.update(status='adopted')
        self.message_user(request, f"{queryset.count()} pets marked as adopted.")
    mark_as_adopted.short_description = "Mark selected pets as adopted"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'saved_pets_count', 'adopted_pets_count', 'liked_pets_count', 'rated_vets_count')
    search_fields = ('user__username', 'user__email', 'phone')
    filter_horizontal = ('saved_pets', 'adopted_pets', 'liked_pets')
    inlines = [RatingInline]
    readonly_fields = ('user',)
    
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
    rated_vets_count.short_description = 'Rated Vets'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'veterinarian', 'score', 'colored_score', 'created_at')
    list_filter = ('score', 'veterinarian', 'created_at')
    search_fields = ('user_profile__user__username', 'veterinarian__name', 'comment')
    date_hierarchy = 'created_at'
    
    def colored_score(self, obj):
        color = 'green' if obj.score >= 4 else 'orange' if obj.score >= 3 else 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.score)
    colored_score.short_description = 'Score'

@admin.register(Walker)
class WalkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'pet_count', 'rate_per_hour', 'is_available')
    search_fields = ('name', 'phone')
    list_filter = ('is_available',)
    filter_horizontal = ('pets',)
    list_editable = ('rate_per_hour', 'is_available')
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Pets'

@admin.register(Hairdresser)
class HairdresserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'pet_count', 'rate_per_session', 'is_available')
    search_fields = ('name', 'phone', 'specialization')
    list_filter = ('is_available',)
    filter_horizontal = ('pets',)
    list_editable = ('rate_per_session', 'is_available')
    
    def pet_count(self, obj):
        return obj.pets.count()
    pet_count.short_description = 'Pets'

# Custom admin site configuration
admin.site.site_header = 'Pet Services Administration'
admin.site.site_title = 'Pet Services Admin Portal'
admin.site.index_title = 'Welcome to Pet Services Admin Portal'