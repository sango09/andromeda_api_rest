"""Tareas de andromeda."""

# Utilidades
import jwt
from datetime import timedelta

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Modelos
from andromeda.users.models import User


def gen_verification_token(user):
    """Crea el token JWT para que el usuario pueda verificar su cuenta."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.email,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


def send_email(content, email_subject, user_pk):
    """Envio de email con los datos asignados a la variable content. """

    user = User.objects.get(pk=user_pk)
    user_token = gen_verification_token(user)
    subject = email_subject
    from_email = f'Andromeda <noreply@andromedapi.tech>'
    name = user.first_name
    content = render_to_string(
        content,
        {'token': user_token, 'user': name}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
