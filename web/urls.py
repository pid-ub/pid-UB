from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from dashboard.view import dashboard_view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', dashboard_view, name="simple_chart"),
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^dashboard/', include('dashboard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
