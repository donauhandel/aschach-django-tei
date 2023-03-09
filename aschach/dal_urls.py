# generated by appcreator
from django.urls import path
from . import dal_views

app_name = "aschach"
urlpatterns = [
    path(
        "angabe-autocomplete/", dal_views.AngabeAC.as_view(), name="angabe-autocomplete"
    ),
    path(
        "fahrzeug-autocomplete/",
        dal_views.FahrzeugAC.as_view(),
        name="fahrzeug-autocomplete",
    ),
    path("firma-autocomplete/", dal_views.FirmaAC.as_view(), name="firma-autocomplete"),
    path(
        "ladung-autocomplete/", dal_views.LadungAC.as_view(), name="ladung-autocomplete"
    ),
    path(
        "nachname-autocomplete/",
        dal_views.NachNameAC.as_view(),
        name="nachname-autocomplete",
    ),
    path("ort-autocomplete/", dal_views.OrtAC.as_view(), name="ort-autocomplete"),
    path(
        "person-autocomplete/", dal_views.PersonAC.as_view(), name="person-autocomplete"
    ),
    path(
        "personangabe-autocomplete/",
        dal_views.PersonAngabeAC.as_view(),
        name="personangabe-autocomplete",
    ),
    path(
        "personladung-autocomplete/",
        dal_views.PersonLadungAC.as_view(),
        name="personladung-autocomplete",
    ),
    path(
        "personenbezeichnung-autocomplete/",
        dal_views.PersonenBezeichnungAC.as_view(),
        name="personenbezeichnung-autocomplete",
    ),
    path(
        "region-autocomplete/", dal_views.RegionAC.as_view(), name="region-autocomplete"
    ),
    path("scan-autocomplete/", dal_views.ScanAC.as_view(), name="scan-autocomplete"),
    path(
        "vorname-autocomplete/",
        dal_views.VorNameAC.as_view(),
        name="vorname-autocomplete",
    ),
    path("ware-autocomplete/", dal_views.WareAC.as_view(), name="ware-autocomplete"),
    path(
        "wareladung-autocomplete/",
        dal_views.WareLadungAC.as_view(),
        name="wareladung-autocomplete",
    ),
]
