import stripe
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.messages import get_messages

class Inicio(TemplateView):
    template_name = "base/inicio.html"
    
    def get(self, request, *args, **kwargs):
        # Consumir los mensajes para que no persistan
        storage = get_messages(request)
        list(storage)  # Esto marca los mensajes como consumidos
        return super().get(request, *args, **kwargs)


class CrearUsuarioView(View):
    template_name = 'base/registrarUsuario.html'  # Nombre del template

    def get(self, request, *args, **kwargs):
        #metodo obligatorio si queremos que tenga post
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Maneja la solicitud POST: procesa el formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        contexto = {
            "usuario":username,
            "email":email,
            "contra":password,
            "verficiar_contra":confirm_password,
        }
        # Validar que las contraseñas coincidan
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, self.template_name, context=contexto)

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, self.template_name, context=contexto)


        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return render(request, self.template_name, context=contexto)


        # Crear el nuevo usuario
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # Iniciar sesión automáticamente al usuario después de registrarse (opcional)
            login(request, user)
            messages.success(request, "Usuario creado exitosamente.")
            return redirect(reverse('inicio'))  # Redirige a la página principal
        except Exception as e:
            messages.error(request, f"Error al crear el usuario: {str(e)}")
            return render(request, self.template_name, context=contexto)


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
