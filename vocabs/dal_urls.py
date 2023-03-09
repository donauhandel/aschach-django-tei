from django.urls import path
from . import dal_views
from .models import SkosLabel, SkosConcept, SkosConceptScheme, SkosCollection

app_name = "vocabs"

urlpatterns = [
    path(
        "skoslabel-autocomplete/",
        dal_views.SkosLabelAC.as_view(
            model=SkosLabel,
            create_field="name",
        ),
        name="skoslabel-autocomplete",
    ),
    path(
        "skoslabel-filter-autocomplete/",
        dal_views.SkosLabelAC.as_view(model=SkosLabel),
        name="skoslabel-filter-autocomplete",
    ),
    path(
        "skosconceptscheme-autocomplete/",
        dal_views.SkosConceptSchemeAC.as_view(
            model=SkosConceptScheme,
            create_field="dc_title",
        ),
        name="skosconceptscheme-autocomplete",
    ),
    path(
        "skoscollection-autocomplete/",
        dal_views.SkosCollectionAC.as_view(
            model=SkosCollection,
            create_field="name",
        ),
        name="skoscollection-autocomplete",
    ),
    path(
        "skosconcept-autocomplete/",
        dal_views.SpecificConcepts.as_view(
            model=SkosConcept,
            create_field="pref_label",
        ),
        name="skosconcept-autocomplete",
    ),
    path(
        "skosconcept-filter-autocomplete/",
        dal_views.SpecificConcepts.as_view(model=SkosConcept),
        name="skosconcept-filter-autocomplete",
    ),
    path(
        "skosconcept-pref-label-autocomplete/",
        dal_views.SkosConceptPrefLabalAC.as_view(),
        name="skosconcept-label-ac",
    ),
    path(
        "skos-constraint-ac/",
        dal_views.SKOSConstraintAC.as_view(model=SkosConcept),
        name="skos-constraint-ac",
    ),
    path(
        "skos-constraint-no-hierarchy-ac/",
        dal_views.SKOSConstraintACNoHierarchy.as_view(model=SkosConcept),
        name="skos-constraint-no-hierarchy-ac",
    ),
    path(
        r"specific-concept-ac/<str:scheme>",
        dal_views.SpecificConcepts.as_view(model=SkosConcept),
        name="specific-concept-ac",
    ),
    path(
        r"concept-by-colleciton-ac/<str:scheme>",
        dal_views.SpecificConceptsByCollection.as_view(model=SkosConcept),
        name="concept-by-collection-ac",
    ),
]
