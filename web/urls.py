from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from dashboard.view import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^home/$', home_view, name="home"),
    url(r'^students/$', students_view, name="students"),
    url(r'^subjects/$', subjects_view, name="subjects"),
    url(r'^about/$', about_view, name="about"),
    url(r'^$', RedirectView.as_view(pattern_name='home', permanent=False))
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
