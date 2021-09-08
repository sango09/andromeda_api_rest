"""Vista de usuarios."""

# Django REST Framework
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

# Modelos
from andromeda.users.models import User
# Permisos
from andromeda.users.permissions import IsAccountOwner
# Serializers
from andromeda.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    EmailResetPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    ContactAndromedaSerializer,
)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """View set de usuarios

    Agrupa las vistas de registro, ingreso y verificación de cuenta.
    """
    serializer_class = UserModelSerializer

    def get_queryset(self):
        return User.objects.filter(
            is_client=True,
        )

    def perform_destroy(self, instance):
        """Inactiva el usuario."""
        instance.is_active = False
        instance.save()

    def get_permissions(self):
        """Permisos basados en la acción."""
        if self.action in ['signup', 'login', 'verify', 'email_reset_password', 'reset_password', 'contact_andromeda']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'change_password']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Ingreso de usuario."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """Registro de usuario."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verificación de cuenta."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Felicitaciones tu cuenta fue verificada!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def profile(self, request, *args, **kwargs):
        """Perfil de usuario."""
        user = self.get_object()
        data = UserModelSerializer(user).data
        return Response(data)

    @action(detail=False, methods=['post'])
    def email_reset_password(self, request):
        """Solicitud de cambio de contraseña."""
        serializer = EmailResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Mensaje enviado'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """Olvido de contraseña."""
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Tu contraseña fue cambiada exitosamente'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Cambio de contraseña."""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Tu contraseña fue cambiada exitosamente'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def contact_andromeda(self, request):
        """Envio de correo para contactar con Andromeda"""
        serializer = ContactAndromedaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Gracias por contactarnos, pronto nos pondremos en contacto contigo'}
        return Response(data, status=status.HTTP_200_OK)
