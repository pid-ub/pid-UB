from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from dashboard.view import dashboard_view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^dashboard/$', dashboard_view, name="dashboard"),
    url(r'^other/$', dashboard_view, name="other"),
    url(r'^about/$', dashboard_view, name="about"),
    url(r'^$', RedirectView.as_view(pattern_name='dashboard', permanent=False))
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^dashboard/', include('dashboard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
