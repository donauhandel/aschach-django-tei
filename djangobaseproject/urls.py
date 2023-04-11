from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from vocabs import api_views

router = routers.DefaultRouter()
router.register(r"metadata", api_views.MetadataViewSet)
router.register(r"skoslabels", api_views.SkosLabelViewSet)
router.register(r"skosnamespaces", api_views.SkosNamespaceViewSet)
router.register(r"skosconceptschemes", api_views.SkosConceptSchemeViewSet)
router.register(r"skoscollections", api_views.SkosCollectionViewSet)
router.register(r"skosconcepts", api_views.SkosConceptViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("browsing/", include("browsing.urls", namespace="browsing")),
    path("aschach/", include("aschach.urls", namespace="aschach")),
    path("aschach-ac/", include("aschach.dal_urls", namespace="aschach-ac")),
    path("info/", include("infos.urls", namespace="info")),
    path("vocabs/", include("vocabs.urls", namespace="vocabs")),
    path("netvis/", include("netvis.urls", namespace="netvis")),
    path("vocabs-ac/", include("vocabs.dal_urls", namespace="vocabs-ac")),
    path("vis/", include("vis.urls", namespace="vis")),
    path("", include("webpage.urls", namespace="webpage")),
]

if "bib" in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("bib/", include("bib.urls", namespace="bib")),
    )

if "sparql" in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("sparql/", include("sparql.urls", namespace="sparql")),
    )

handler404 = "webpage.views.handler404"
