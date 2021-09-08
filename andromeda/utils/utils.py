"""Utilidades de andromeda."""

# Utilidades
import io
import random

# Graficos
import matplotlib.pyplot as plt

# Django
from django.http import HttpResponse

# Modelos
from andromeda.roles.assistant.models import Assistant


def get_image():
    """Genera la imagen con una respuesta."""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Length'] = str(len(response.content))
    buffer.close()
    return response


def get_assistant_asigned():
    """Asigna el auxiliar de sistemas para el servicio solicitado."""
    first_assistant = Assistant.objects.filter(availability=True).first().pk
    last_assistant = Assistant.objects.filter(availability=True).last().pk + 1
    try:
        assistant = Assistant.objects.get(id=random.randrange(first_assistant, last_assistant))
    except Assistant.DoesNotExist:
        assistant = get_assistant_asigned()
    return assistant
