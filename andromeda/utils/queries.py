"""Consultas para los reportes PDF."""

# Utilidades
import collections

# Modelos
from andromeda.modules.loans.models import Loans
from andromeda.roles.assistant.models import Assistant


def get_total_implements():
    """Obtiene los implementos totales solicitados en prestamos."""
    total_implements = 0
    for i in Loans.objects.all():
        total_implements += i.ammount_implements
    return total_implements


def get_best_auxiliary(Model):
    """Obtiene el auxiliar mas asignado en el servicio de prestamos tecnologicos."""
    try:
        assistants = Model.objects.values_list('assigned_auxiliary', flat=True)
        assistant_most_common = Assistant.objects.get(pk=collections.Counter(assistants).most_common(1)[0][0])
        return assistant_most_common

    except IndexError:
        return 'Sin auxiliares'
