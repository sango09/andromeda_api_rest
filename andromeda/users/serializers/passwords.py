"""Serializer de contraseñas."""

# Utilidades
import jwt
from django.conf import settings
# Django
from django.contrib.auth import password_validation
from django.core.exceptions import ObjectDoesNotExist
# Django REST Framework
from rest_framework import serializers

# Tareas
from andromeda.tasks.tasks import send_email
# Modelos
from andromeda.users.models import User


def update_password(email, passd):
    """Actualiza la contraseña actual del usuario."""
    user = User.objects.get(email=email)
    user.set_password(passd)
    user.save()


def validate_password(data):
    """Verifica que las contraseñas coincidan."""
    passwd = data['new_password']
    passwd_conf = data['new_password_confirmation']
    if passwd != passwd_conf:
        raise serializers.ValidationError('Las contraseñas no coinciden')
    password_validation.validate_password(passwd)
    return data


class EmailResetPasswordSerializer(serializers.Serializer):
    """Serializer que envia el email con el token para cambiar la contraseña."""
    email = serializers.EmailField()

    def create(self, data):
        """Envia el email al usuario"""
        user = User.objects.get(**data)
        send_email(content='emails/users/reset_password.html',
                   email_subject='Recupera tu contraseña',
                   user_pk=user.pk)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer para cambiar la contraseña del usuario."""
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirmation = serializers.CharField(min_length=8)

    def validate_token(self, data):
        """Verifica que el token sea valido."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('El token expiro')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Token Invalido')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Token invalido')

        self.context['payload'] = payload
        return data

    def validate(self, data):
        """Validación de las contraseñas."""
        return validate_password(data)

    def create(self, data):
        """Actualiza la contraseña del usuario."""
        payload = self.context['payload']
        try:
            passw = data['new_password']
            update_password(payload['user'], passw)
            return data

        except ObjectDoesNotExist:
            raise serializers.ValidationError('Cuenta invalida')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar la contraseña actual."""
    email = serializers.EmailField()
    old_password = serializers.CharField(min_length=8)
    new_password = serializers.CharField(min_length=8)
    new_password_confirmation = serializers.CharField(min_length=8)

    def validate(self, data):
        """Validación de contraseñas."""
        return validate_password(data)

    def create(self, data):
        """Actualiza la contraseña del usuario."""
        email = data['email']
        passw = data['new_password']
        old_passwd = data['old_password']
        try:
            if not User.objects.get(email=email).check_password(old_passwd):
                raise serializers.ValidationError('Contraseña invalida')
            update_password(email, passw)
            return data

        except ObjectDoesNotExist:
            raise serializers.ValidationError('Cuenta invalida')
