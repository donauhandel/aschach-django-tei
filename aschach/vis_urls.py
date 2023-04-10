from django.urls import path
from . import vis_views

app_name = "aschach"


urlpatterns = [
    path('angabe-by-date/<slug:by>', vis_views.angabe_by_date_view, name='angabe_by_date'),
]
