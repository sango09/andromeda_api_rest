"""Serializer de usuarios."""

# Utilidades
import jwt
from django.conf import settings
# Django
from django.contrib.auth import password_validation, authenticate
from django.core.exceptions import ObjectDoesNotExist
# Django REST Framework
from django.core.mail import EmailMultiAlternatives
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from andromeda.roles.assistant.models import Assistant
from andromeda.roles.assistant.serializers import AssistantModelSerializer
from andromeda.roles.employee.models import Employee
from andromeda.roles.employee.serializers import EmployeeModelSerializer
# Tareas
from andromeda.tasks.tasks import send_email
# Modelos
from andromeda.users.models import User, Profile
# Serializers
from andromeda.users.serializers.profiles import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """Serializer de usuarios."""
    profile = ProfileModelSerializer()
    employee = EmployeeModelSerializer()
    assistant = AssistantModelSerializer()

    class Meta:
        """Clase meta."""
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_admin',
            'is_assistant',
            'is_employee',
            'is_verified',
            'is_active',
            'profile',
            'employee',
            'assistant',
        )

    def update(self, instance, validated_data):
        """Actualiza los datos del usuario incluyendo el perfil asignado."""
        if validated_data.get('profile'):
            profile_data = validated_data.get('profile')
            profile_serializer = ProfileModelSerializer(data=profile_data)

            if profile_serializer.is_valid():
                profile = profile_serializer.update(instance=instance.profile, validated_data=profile_data)
                validated_data['profile'] = profile

        return super(UserModelSerializer, self).update(instance, validated_data)


class UserSignUpSerializer(serializers.Serializer):
    """Registro de usuarios

    Los usuarios se podran registrar con su rol especificado
    y se les asiganara un unico perfil.
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=5,
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8)

    first_name = serializers.CharField(min_length=2, max_length=25)
    last_name = serializers.CharField(min_length=2, max_length=25)

    is_admin = serializers.BooleanField(default=False)
    is_employee = serializers.BooleanField(default=False)
    is_assistant = serializers.BooleanField(default=False)

    def validate(self, data):
        """Verifica que las contraseñas coincidan."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Crea el usuario y le asigna un perfil."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)

        if user.is_employee:
            Employee.objects.create(user=user)

        elif user.is_assistant:
            Assistant.objects.create(user=user)

        send_email(content='emails/users/account_verification.html',
                   email_subject=f'Bienvenido {user.username}! a Andromeda',
                   user_pk=user.pk)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer para el ingreso de usuarios

    Valida los datos ingresados por el usuario con los datos de la base de datos.
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        """Valida credenciales de acceso."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales invalidas')
        if not user.is_verified:
            raise serializers.ValidationError('Tu cuenta aun no esta verificada :(')
        self.context['user'] = user
        return data

    def create(self, validated_data):
        """Genera o recibe el token de autenticación."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Serialzier para la verificación de cuenta."""
    token = serializers.CharField()

    def validate_token(self, data):
        """Verifica que el token sea valido."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('La verificación ha expirado')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Token Invalido')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Token Invalido')

        self.context['payload'] = payload
        return data

    def save(self):
        """Actualiza el estado de verificado del usuario."""
        payload = self.context['payload']
        try:
            user = User.objects.get(email=payload['user'])
            user.is_verified = True
            user.save()
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Cuenta invalida')


class ContactAndromedaSerializer(serializers.Serializer):
    """Serializer para contacto con Andromeda."""
    full_name = serializers.CharField(max_length=50)
    from_email = serializers.EmailField()
    subject = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=200)

    def create(self, data):
        """Envio de mensaje"""
        email_subject = f'{data["from_email"]} a enviado un mensaje'
        to = 'andromedamaster6@gmail.com'
        from_email = f'{data["full_name"]} <noreply@andromedapi.tech>'
        msg = EmailMultiAlternatives(email_subject, data['message'], from_email, [to])
        msg.send()
        return data
