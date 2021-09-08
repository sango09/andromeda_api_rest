"""Genera los reportes de los modulos."""

# Utilidades
import collections
import functools
import ssl
import sys

# matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Pandas
import pandas as pd

# Django
from django.http.response import Http404
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils import timezone
from django.views.generic import (
    ListView,
)

# Django Weasyprint
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.utils import django_url_fetcher
from django_weasyprint.views import WeasyTemplateResponse

# Modelos
from andromeda.modules.inventory.models import Inventory, TechnicalDataSheet
from andromeda.modules.loans.models import Loans, InventoryLoans
from andromeda.modules.maintenance.models import Maintenance
from andromeda.modules.technical_support.models import Support
from andromeda.users.models import User
# Consultas
from andromeda.utils.queries import (
    get_total_implements,
    get_best_auxiliary,
)
from andromeda.utils.utils import get_image


def str_to_class(module):
    """Obtiene el modelo de la clase ingresada en el path."""
    return getattr(sys.modules[__name__], module)


class ReportListView(ListView):
    """List View de reportes,"""

    def dispatch(self, request, *args, **kwargs):
        try:
            # Template
            self.template_name = 'PDF/modules/{}/report.html'.format(self.kwargs['module'])
            get_template(self.template_name)
            # Model
            self.model = str_to_class(self.kwargs['module'].capitalize())

            return super(ReportListView, self).dispatch(request, *args, *kwargs)

        except TemplateDoesNotExist:
            raise Http404
        except AttributeError:
            raise Http404

    def get_context_data(self, **kwargs):
        """Contexto de datos."""
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()

        if self.kwargs['module'] == 'loans':
            # Datos para prestamos
            context['total_loans'] = Loans.objects.count()
            context['implements_total'] = get_total_implements()
            context['best'] = get_best_auxiliary(Loans)

        elif self.kwargs['module'] == 'inventory':
            # Datos de inventario
            context['implements_total'] = Inventory.objects.count()
            context['tech_tabs_total'] = TechnicalDataSheet.objects.count()
            context['disabled_implements'] = Inventory.objects.filter(status_implement='Inactivo').count()

        elif self.kwargs['module'] == 'maintenance':
            # Datos de mantenimiento
            context['maintenance_total'] = Maintenance.objects.filter(is_active=False).count()
            context['implements_maintenance_total'] = Inventory.objects.filter(status_implement='En mantenimiento').count()
            context['best_auxiliary_maintenance'] = get_best_auxiliary(Maintenance)

        elif self.kwargs['module'] == 'support':
            context['supports_completed'] = Support.objects.filter(status_support='Completado').count()
            context['supports_total'] = Support.objects.count()
            context['best_auxiliary_support'] = get_best_auxiliary(Support)
        else:
            context['module'] = True
        return context


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to change the default URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)


class PrintReportView(WeasyTemplateResponseMixin, ReportListView):
    """Renderiza el template como pdf"""
    pdf_attachment = True
    response_class = CustomWeasyTemplateResponse

    def get_pdf_filename(self):
        return f"andromeda-{timezone.now().strftime('%Y%m%d-%H%M')}.pdf"


def most_requested_implements(request):
    """Grafico de los implementos mas solicitados por los usuarios."""

    data = Loans.objects.values_list('implement', flat=True)
    implements = collections.Counter(data)
    names = []

    for implement_id in implements.keys():
        x = InventoryLoans.objects.get(pk=implement_id)
        names.append(x.implement.name)

    values = list(implements.values())
    fig, axs = plt.subplots(figsize=(10, 4))
    axs.yaxis.set_major_locator(MaxNLocator(integer=True))
    axs.set_ylabel("Solicitudes")
    axs.bar(names, values)
    fig.suptitle('Implementos mas solicitados')
    return get_image()


def graph_users(request):
    """Grafico plot del modelo de usuarios."""
    user = User.objects.all().values()
    df = pd.DataFrame(user, columns=['date_joined'])
    data = df['date_joined'].dt.month_name().value_counts()
    data = data.sort_values(ascending=True)
    data.plot.bar(xlabel="Mes", ylabel="Usuarios", figsize=(8, 8))
    return get_image()
