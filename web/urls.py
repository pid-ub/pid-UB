from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from dashboard.view import *

urlpatterns = patterns(
    '',
    url(r'^$', home_view, name="home"),
    url(r'^home/$', RedirectView.as_view(pattern_name='home', permanent=False)),
    url(r'^students/$', students_view, name="students"),
    url(r'^subjects/$', subjects_view, name="subjects"),
    url(r'^predictive/$', predictive_view, name="predictive"),
    url(r'^team/$', team_view, name="team")
)
