import stripe
import json
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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

# Configurar logging
logger = logging.getLogger(__name__)

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
        
        # Obtener el correo electrónico del usuario si está autenticado
        customer_email = None
        if request.user.is_authenticated:
            customer_email = request.user.email
        
        # Crear la sesión de Stripe
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
            customer_email=customer_email,  # Añadir el correo del cliente si está disponible
            success_url=request.build_absolute_uri(reverse('pago_exitoso')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('pago_cancelado')),
        )
        
        return JsonResponse({"id": session.id})

class PagoExitoso(TemplateView):
    template_name = "base/pago_exitoso.html"
    
    def get(self, request, *args, **kwargs):
        # Obtener el ID de la sesión de Stripe
        session_id = request.GET.get('session_id')
        
        if session_id:
            try:
                # Recuperar la información de la sesión de Stripe
                stripe.api_key = settings.STRIPE_SECRET_KEY
                session = stripe.checkout.Session.retrieve(session_id)
                
                # Obtener el correo electrónico del cliente
                customer_email = session.customer_details.email
                customer_name = session.customer_details.name or 'Cliente'
                
                # Enviar correo electrónico de confirmación
                if customer_email:
                    try:
                        self.enviar_correo_confirmacion(customer_email, customer_name)
                        messages.success(request, f"Se ha enviado un correo de confirmación a {customer_email}")
                    except Exception as e:
                        logger.error(f"Error al enviar correo: {str(e)}")
                        messages.warning(request, "El pago se procesó correctamente, pero hubo un problema al enviar el correo de confirmación.")
            except Exception as e:
                logger.error(f"Error al procesar el pago: {str(e)}")
                messages.error(request, "Hubo un problema al procesar la información del pago.")
        
        return super().get(request, *args, **kwargs)
    
    def enviar_correo_confirmacion(self, email, nombre):
        """Envía un correo electrónico de confirmación al cliente."""
        # Usar un asunto simple sin caracteres especiales para evitar problemas de codificación
        asunto = 'Confirmacion de Pago - PetHome'
        
        # Contexto para la plantilla
        contexto = {
            'nombre': nombre,
        }
        
        try:
            print(f"Enviando correo a: {email}")
            print(f"Nombre del cliente: {nombre}")
            print(f"Codificación del nombre: {nombre.encode('utf-8')}")
            # Renderizar el correo HTML
            html_message = render_to_string('base/email/pago_exitoso_email.html', contexto)
            plain_message = strip_tags(html_message)
            
            # Crear el mensaje de correo
            msg = EmailMultiAlternatives(
                subject=asunto,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            
            # Adjuntar la versión HTML
            msg.attach_alternative(html_message, "text/html")
            
            # Enviar el correo
            msg.send(fail_silently=False)
            
            logger.info(f"Correo enviado exitosamente a {email}")
            
        except Exception as e:
            logger.error(f"Error en enviar_correo_confirmacion: {str(e)}")
            raise

class PagoCancelado(TemplateView):
    template_name = "base/pago_cancelado.html"