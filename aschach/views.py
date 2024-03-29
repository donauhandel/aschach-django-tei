# generated by appcreator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .filters import (
    AngabeListFilter,
    FahrzeugListFilter,
    FirmaListFilter,
    LadungListFilter,
    NachNameListFilter,
    OrtListFilter,
    PersonListFilter,
    PersonAngabeListFilter,
    PersonLadungListFilter,
    PersonenBezeichnungListFilter,
    RegionListFilter,
    ScanListFilter,
    VorNameListFilter,
    WareListFilter,
    WareLadungListFilter,
)
from .forms import (
    AngabeForm,
    FahrzeugForm,
    FirmaForm,
    LadungForm,
    NachNameForm,
    OrtForm,
    PersonForm,
    PersonAngabeForm,
    PersonLadungForm,
    PersonenBezeichnungForm,
    RegionForm,
    ScanForm,
    VorNameForm,
    WareForm,
    WareLadungForm,
    AngabeFilterFormHelper,
    FahrzeugFilterFormHelper,
    FirmaFilterFormHelper,
    LadungFilterFormHelper,
    NachNameFilterFormHelper,
    OrtFilterFormHelper,
    PersonFilterFormHelper,
    PersonAngabeFilterFormHelper,
    PersonLadungFilterFormHelper,
    PersonenBezeichnungFilterFormHelper,
    RegionFilterFormHelper,
    ScanFilterFormHelper,
    VorNameFilterFormHelper,
    WareFilterFormHelper,
    WareLadungFilterFormHelper,
)
from .tables import (
    AngabeTable,
    FahrzeugTable,
    FirmaTable,
    LadungTable,
    NachNameTable,
    OrtTable,
    PersonTable,
    PersonAngabeTable,
    PersonLadungTable,
    PersonenBezeichnungTable,
    RegionTable,
    ScanTable,
    VorNameTable,
    WareTable,
    WareLadungTable,
)
from .models import (
    Angabe,
    Fahrzeug,
    Firma,
    Ladung,
    NachName,
    Ort,
    Person,
    PersonAngabe,
    PersonLadung,
    PersonenBezeichnung,
    Region,
    Scan,
    VorName,
    Ware,
    WareLadung,
)
from browsing.browsing_utils import (
    GenericListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDetailView,
)


class AngabeListView(GenericListView):
    model = Angabe
    filter_class = AngabeListFilter
    formhelper_class = AngabeFilterFormHelper
    table_class = AngabeTable
    init_columns = [
        "legacy_pk",
        "datum",
        "related_good",
        "related_person",
        "related_place",
    ]
    exclude_columns = [
        "bemerkungen",
        "eiskalt",
        "fahrzeug",
        "hochwasser",
        "ladung",
        "nichts",
        "orig_data_csv",
    ]
    template_name = "aschach/custom_list.html"


class AngabeDetailView(BaseDetailView):
    model = Angabe
    template_name = "aschach/angabe_detail.html"


class AngabeCreate(BaseCreateView):
    model = Angabe
    form_class = AngabeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AngabeCreate, self).dispatch(*args, **kwargs)


class AngabeUpdate(BaseUpdateView):
    model = Angabe
    form_class = AngabeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AngabeUpdate, self).dispatch(*args, **kwargs)


class AngabeDelete(DeleteView):
    model = Angabe
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:angabe_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AngabeDelete, self).dispatch(*args, **kwargs)


class FahrzeugListView(GenericListView):
    model = Fahrzeug
    filter_class = FahrzeugListFilter
    formhelper_class = FahrzeugFilterFormHelper
    table_class = FahrzeugTable
    init_columns = [
        "id",
        "id",
    ]


class FahrzeugDetailView(BaseDetailView):
    model = Fahrzeug
    template_name = "browsing/generic_detail.html"


class FahrzeugCreate(BaseCreateView):
    model = Fahrzeug
    form_class = FahrzeugForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FahrzeugCreate, self).dispatch(*args, **kwargs)


class FahrzeugUpdate(BaseUpdateView):
    model = Fahrzeug
    form_class = FahrzeugForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FahrzeugUpdate, self).dispatch(*args, **kwargs)


class FahrzeugDelete(DeleteView):
    model = Fahrzeug
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:fahrzeug_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FahrzeugDelete, self).dispatch(*args, **kwargs)


class FirmaListView(GenericListView):
    model = Firma
    filter_class = FirmaListFilter
    formhelper_class = FirmaFilterFormHelper
    table_class = FirmaTable
    init_columns = [
        "id",
        "name",
    ]


class FirmaDetailView(BaseDetailView):
    model = Firma
    template_name = "browsing/generic_detail.html"


class FirmaCreate(BaseCreateView):
    model = Firma
    form_class = FirmaForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FirmaCreate, self).dispatch(*args, **kwargs)


class FirmaUpdate(BaseUpdateView):
    model = Firma
    form_class = FirmaForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FirmaUpdate, self).dispatch(*args, **kwargs)


class FirmaDelete(DeleteView):
    model = Firma
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:firma_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FirmaDelete, self).dispatch(*args, **kwargs)


class LadungListView(GenericListView):
    model = Ladung
    filter_class = LadungListFilter
    formhelper_class = LadungFilterFormHelper
    table_class = LadungTable
    init_columns = [
        "id",
        "angabe",
        "waren",
        "personen"
    ]
    template_name = "aschach/custom_list.html"


class LadungDetailView(BaseDetailView):
    model = Ladung
    template_name = "aschach/ladung_detail.html"


class LadungCreate(BaseCreateView):
    model = Ladung
    form_class = LadungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LadungCreate, self).dispatch(*args, **kwargs)


class LadungUpdate(BaseUpdateView):
    model = Ladung
    form_class = LadungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LadungUpdate, self).dispatch(*args, **kwargs)


class LadungDelete(DeleteView):
    model = Ladung
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:ladung_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LadungDelete, self).dispatch(*args, **kwargs)


class NachNameListView(GenericListView):
    model = NachName
    filter_class = NachNameListFilter
    formhelper_class = NachNameFilterFormHelper
    table_class = NachNameTable
    init_columns = [
        "id",
        "name",
    ]


class NachNameDetailView(BaseDetailView):
    model = NachName
    template_name = "browsing/generic_detail.html"


class NachNameCreate(BaseCreateView):
    model = NachName
    form_class = NachNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NachNameCreate, self).dispatch(*args, **kwargs)


class NachNameUpdate(BaseUpdateView):
    model = NachName
    form_class = NachNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NachNameUpdate, self).dispatch(*args, **kwargs)


class NachNameDelete(DeleteView):
    model = NachName
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:nachname_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NachNameDelete, self).dispatch(*args, **kwargs)


class OrtListView(GenericListView):
    model = Ort
    filter_class = OrtListFilter
    formhelper_class = OrtFilterFormHelper
    table_class = OrtTable
    init_columns = [
        "id",
        "name",
    ]
    template_name = "aschach/custom_list.html"


class OrtDetailView(BaseDetailView):
    model = Ort
    template_name = "aschach/ort_detail.html"


class OrtCreate(BaseCreateView):
    model = Ort
    form_class = OrtForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrtCreate, self).dispatch(*args, **kwargs)


class OrtUpdate(BaseUpdateView):
    model = Ort
    form_class = OrtForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrtUpdate, self).dispatch(*args, **kwargs)


class OrtDelete(DeleteView):
    model = Ort
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:ort_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrtDelete, self).dispatch(*args, **kwargs)


class PersonListView(GenericListView):
    model = Person
    filter_class = PersonListFilter
    formhelper_class = PersonFilterFormHelper
    table_class = PersonTable
    init_columns = [
        "id",
        "has_title",
    ]
    template_name = "aschach/custom_list.html"


class PersonDetailView(BaseDetailView):
    model = Person
    template_name = "aschach/person_detail.html"


class PersonCreate(BaseCreateView):
    model = Person
    form_class = PersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonCreate, self).dispatch(*args, **kwargs)


class PersonUpdate(BaseUpdateView):
    model = Person
    form_class = PersonForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonUpdate, self).dispatch(*args, **kwargs)


class PersonDelete(DeleteView):
    model = Person
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:person_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonDelete, self).dispatch(*args, **kwargs)


class PersonAngabeListView(GenericListView):
    model = PersonAngabe
    filter_class = PersonAngabeListFilter
    formhelper_class = PersonAngabeFilterFormHelper
    table_class = PersonAngabeTable
    init_columns = [
        "id",
        "id",
    ]


class PersonAngabeDetailView(BaseDetailView):
    model = PersonAngabe
    template_name = "browsing/generic_detail.html"


class PersonAngabeCreate(BaseCreateView):
    model = PersonAngabe
    form_class = PersonAngabeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonAngabeCreate, self).dispatch(*args, **kwargs)


class PersonAngabeUpdate(BaseUpdateView):
    model = PersonAngabe
    form_class = PersonAngabeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonAngabeUpdate, self).dispatch(*args, **kwargs)


class PersonAngabeDelete(DeleteView):
    model = PersonAngabe
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:personangabe_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonAngabeDelete, self).dispatch(*args, **kwargs)


class PersonLadungListView(GenericListView):
    model = PersonLadung
    filter_class = PersonLadungListFilter
    formhelper_class = PersonLadungFilterFormHelper
    table_class = PersonLadungTable
    init_columns = [
        "id",
        "id",
    ]


class PersonLadungDetailView(BaseDetailView):
    model = PersonLadung
    template_name = "browsing/generic_detail.html"


class PersonLadungCreate(BaseCreateView):
    model = PersonLadung
    form_class = PersonLadungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonLadungCreate, self).dispatch(*args, **kwargs)


class PersonLadungUpdate(BaseUpdateView):
    model = PersonLadung
    form_class = PersonLadungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonLadungUpdate, self).dispatch(*args, **kwargs)


class PersonLadungDelete(DeleteView):
    model = PersonLadung
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:personladung_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonLadungDelete, self).dispatch(*args, **kwargs)


class PersonenBezeichnungListView(GenericListView):
    model = PersonenBezeichnung
    filter_class = PersonenBezeichnungListFilter
    formhelper_class = PersonenBezeichnungFilterFormHelper
    table_class = PersonenBezeichnungTable
    init_columns = [
        "id",
        "bezeichnung",
    ]


class PersonenBezeichnungDetailView(BaseDetailView):
    model = PersonenBezeichnung
    template_name = "browsing/generic_detail.html"


class PersonenBezeichnungCreate(BaseCreateView):
    model = PersonenBezeichnung
    form_class = PersonenBezeichnungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonenBezeichnungCreate, self).dispatch(*args, **kwargs)


class PersonenBezeichnungUpdate(BaseUpdateView):
    model = PersonenBezeichnung
    form_class = PersonenBezeichnungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonenBezeichnungUpdate, self).dispatch(*args, **kwargs)


class PersonenBezeichnungDelete(DeleteView):
    model = PersonenBezeichnung
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:personenbezeichnung_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonenBezeichnungDelete, self).dispatch(*args, **kwargs)


class RegionListView(GenericListView):
    model = Region
    filter_class = RegionListFilter
    formhelper_class = RegionFilterFormHelper
    table_class = RegionTable
    init_columns = [
        "id",
        "name",
    ]
    template_name = "aschach/custom_list.html"


class RegionDetailView(BaseDetailView):
    model = Region
    template_name = "aschach/region_detail.html"


class RegionCreate(BaseCreateView):
    model = Region
    form_class = RegionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegionCreate, self).dispatch(*args, **kwargs)


class RegionUpdate(BaseUpdateView):
    model = Region
    form_class = RegionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegionUpdate, self).dispatch(*args, **kwargs)


class RegionDelete(DeleteView):
    model = Region
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:region_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegionDelete, self).dispatch(*args, **kwargs)


class ScanListView(GenericListView):
    model = Scan
    filter_class = ScanListFilter
    formhelper_class = ScanFilterFormHelper
    table_class = ScanTable
    init_columns = [
        "id",
        "datei_name",
    ]


class ScanDetailView(BaseDetailView):
    model = Scan
    template_name = "browsing/generic_detail.html"


class ScanCreate(BaseCreateView):
    model = Scan
    form_class = ScanForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScanCreate, self).dispatch(*args, **kwargs)


class ScanUpdate(BaseUpdateView):
    model = Scan
    form_class = ScanForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScanUpdate, self).dispatch(*args, **kwargs)


class ScanDelete(DeleteView):
    model = Scan
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:scan_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScanDelete, self).dispatch(*args, **kwargs)


class VorNameListView(GenericListView):
    model = VorName
    filter_class = VorNameListFilter
    formhelper_class = VorNameFilterFormHelper
    table_class = VorNameTable
    init_columns = [
        "id",
        "name",
    ]


class VorNameDetailView(BaseDetailView):
    model = VorName
    template_name = "browsing/generic_detail.html"


class VorNameCreate(BaseCreateView):
    model = VorName
    form_class = VorNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VorNameCreate, self).dispatch(*args, **kwargs)


class VorNameUpdate(BaseUpdateView):
    model = VorName
    form_class = VorNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VorNameUpdate, self).dispatch(*args, **kwargs)


class VorNameDelete(DeleteView):
    model = VorName
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:vorname_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VorNameDelete, self).dispatch(*args, **kwargs)


class WareListView(GenericListView):
    model = Ware
    filter_class = WareListFilter
    formhelper_class = WareFilterFormHelper
    table_class = WareTable
    init_columns = [
        "id",
        "name",
        "beschreibung",
        "name_orig"
    ]
    template_name = "aschach/custom_list.html"
    excluded_cols = [
        "legacy_id",
        "orig_data_csv"
    ]


class WareDetailView(BaseDetailView):
    model = Ware
    template_name = "aschach/ware_detail.html"


class WareCreate(BaseCreateView):
    model = Ware
    form_class = WareForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareCreate, self).dispatch(*args, **kwargs)


class WareUpdate(BaseUpdateView):
    model = Ware
    form_class = WareForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareUpdate, self).dispatch(*args, **kwargs)


class WareDelete(DeleteView):
    model = Ware
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:ware_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareDelete, self).dispatch(*args, **kwargs)


class WareLadungListView(GenericListView):
    model = WareLadung
    filter_class = WareLadungListFilter
    formhelper_class = WareLadungFilterFormHelper
    table_class = WareLadungTable
    init_columns = [
        "id",
    ]
    template_name = "aschach/custom_list.html"


class WareLadungDetailView(BaseDetailView):
    model = WareLadung
    template_name = "browsing/generic_detail.html"


class WareLadungCreate(BaseCreateView):
    model = WareLadung
    form_class = WareLadungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareLadungCreate, self).dispatch(*args, **kwargs)


class WareLadungUpdate(BaseUpdateView):
    model = WareLadung
    form_class = WareLadungForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareLadungUpdate, self).dispatch(*args, **kwargs)


class WareLadungDelete(DeleteView):
    model = WareLadung
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("aschach:wareladung_browse")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareLadungDelete, self).dispatch(*args, **kwargs)
