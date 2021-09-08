"""Main URLs module."""

# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

# Vistas
from andromeda.tasks.reports import report
from andromeda.tasks.reports.report import graph_users

urlpatterns = [
                  # Django Admin
                  path('admin/', admin.site.urls),

                  # Roles and users
                  path('api/', include(('andromeda.users.urls', 'users'), namespace='users')),
                  path('api/', include(('andromeda.roles.assistant.urls', 'assistant'), namespace='assistant')),
                  path('api/', include(('andromeda.roles.employee.urls', 'employee'), namespace='employee')),

                  # Modules
                  path('api/', include(('andromeda.modules.inventory.urls', 'inventory'), namespace='inventory')),
                  path('api/', include(('andromeda.modules.loans.urls', 'loans'), namespace='loans')),
                  path('api/', include(('andromeda.modules.technical_support.urls', 'supports'), namespace='supports')),
                  path('api/', include(('andromeda.modules.maintenance.urls', 'maintenance'), namespace='maintenance')),

                  # PDF
                  path(
                      route='pdf/report/<module>/',
                      view=report.PrintReportView.as_view(),
                      name='reports'
                  ),
                  # Graficos
                  path(
                      route='most_requested_implements/',
                      view=report.most_requested_implements,
                      name='implementos_mas_solicitados'
                  ),
                  path(
                      route="grafico/",
                      view=graph_users,
                      name='grafico'
                  ),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
