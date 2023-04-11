from django.urls import path
from . import views

app_name = "vis"


urlpatterns = [
    path('angabe-by-date/<slug:by>', views.angabe_by_date_view, name='angabe_by_date'),
    path('angabe-over-time/<slug:by>', views.AngabeOverTimeView.as_view(), name='angabe_over_time'),
]
