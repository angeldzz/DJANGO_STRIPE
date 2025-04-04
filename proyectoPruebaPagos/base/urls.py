from django.urls import path
from . import views

urlpatterns = [
    path("", views.Inicio.as_view(), name="inicio"),
    path("create-checkout-session/", views.CreateCheckoutSessionView.as_view(), name="checkout"),
    path("crear-usuario/", views.CrearUsuarioView.as_view(), name="crear_usuario"),
    path("pago-exitoso/", views.PagoExitoso.as_view(), name="pago_exitoso"),
    path("pago-cancelado/", views.PagoCancelado.as_view(), name="pago_cancelado"),
]