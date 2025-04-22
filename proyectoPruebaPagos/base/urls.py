# base/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear un enrutador para las APIs
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'veterinarians', views.VeterinarianViewSet)
router.register(r'veterinary-clinics', views.VeterinaryClinicViewSet)
router.register(r'shelters', views.ShelterViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'pets', views.PetViewSet)
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'ratings', views.RatingViewSet)
router.register(r'walkers', views.WalkerViewSet)
router.register(r'hairdressers', views.HairdresserViewSet)

urlpatterns = [
    path("", views.Inicio.as_view(), name="inicio"),
    path("create-checkout-session/", views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path("crear-usuario/", views.CrearUsuarioView.as_view(), name="crear_usuario"),
    path("pago-exitoso/", views.PagoExitoso.as_view(), name="pago_exitoso"),
    path("pago-cancelado/", views.PagoCancelado.as_view(), name="pago_cancelado"),
    path("api/", include(router.urls)),  # Incluye las rutas de la API
]