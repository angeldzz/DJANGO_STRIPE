from django.urls import path
from .views import Inicio, CreateCheckoutSessionView,PagoCancelado,PagoExitoso

urlpatterns = [
    path("", Inicio.as_view(), name="inicio"),
    path("create-checkout-session/", CreateCheckoutSessionView.as_view(), name="checkout"),
    path("pago-exitoso/", PagoExitoso.as_view(), name="pago_exitoso"),
    path("pago-cancelado/", PagoCancelado.as_view(), name="pago_cancelado"),
]