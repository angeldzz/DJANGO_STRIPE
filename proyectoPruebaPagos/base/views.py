import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView

class Inicio(TemplateView):
    template_name = "base/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        return context

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": "Paseo de 1 hora"},
                        "unit_amount": 2500,  # Precio en centimos (25 EUR)
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="http://localhost:8000/pago-exitoso/",
            cancel_url="http://localhost:8000/pago-cancelado/",
        )
        return JsonResponse({"id": session.id})

class PagoExitoso(TemplateView):
    template_name = "base/pago_exitoso.html"

class PagoCancelado(TemplateView):
    template_name = "base/pago_cancelado.html"
