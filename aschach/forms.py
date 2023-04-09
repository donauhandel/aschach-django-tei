# generated by appcreator
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from crispy_forms.bootstrap import Accordion, AccordionGroup

from vocabs.models import SkosConcept
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


class AngabeFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AngabeFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.form_tag = False
        self.layout = Layout(
            Fieldset(
                "",
                "id",
                "legacy_id",
                "related_good",
                "related_person",
                "related_place",
                css_id="basic_search_fields",
            ),
        )


class AngabeForm(forms.ModelForm):
    class Meta:
        model = Angabe
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AngabeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class FahrzeugFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FahrzeugFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "person",
                    "herkunft",
                    "region",
                    "fahrtrichtung",
                    "bemerkungen",
                    "anzahl_pferde",
                    "hohenau",
                    "zielort",
                    "zurueck",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class FahrzeugForm(forms.ModelForm):
    fahrtrichtung = forms.ModelChoiceField(
        required=False,
        label="Fahrtrichtung",
        queryset=SkosConcept.objects.filter(collection__name="fahrtrichtung"),
    )

    class Meta:
        model = Fahrzeug
        fields = ["id", "fahrtrichtung"]

    def __init__(self, *args, **kwargs):
        super(FahrzeugForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class FirmaFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FirmaFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "name",
                    "bemerkungen",
                    "name_orig",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class FirmaForm(forms.ModelForm):
    class Meta:
        model = Firma
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(FirmaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class LadungFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LadungFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "bemerkungen",
                    "dreilingsgeld",
                    "kammergut",
                    "mautbefreiung",
                    "mautbefreiung_all",
                    "niederlage",
                    "passbrief",
                    "per_kommission",
                    "per_schiffmeister",
                    "per_schiffukgut",
                    "personen",
                    "waren",
                    "weitertransport",
                    "zielort",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class LadungForm(forms.ModelForm):
    class Meta:
        model = Ladung
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(LadungForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class NachNameFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NachNameFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search", "name", "bemerkungen", "name_orig", css_id="more"
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class NachNameForm(forms.ModelForm):
    class Meta:
        model = NachName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NachNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class OrtFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OrtFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "name",
                    "bemerkungen",
                    "literatur",
                    "name_orig",
                    "region",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class OrtForm(forms.ModelForm):
    class Meta:
        model = Ort
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OrtForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class PersonFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset(
                "",
                "legacy_pk",
                "nachname",
                "vorname",
                "firma",
                "bezeichnung",
                "bemerkungen",
                "weiblich",
                "herkunft",
                "jude",
                "verknuepft",
                "id",
                css_id="basic_search_fields",
            ),
        )


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class PersonAngabeFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonAngabeFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "person",
                    "angabe",
                    "bemerkungen",
                    "judenleibmaut",
                    "judenleibmaut_fl",
                    "judenleibmaut_s",
                    "judenleibmaut_d",
                    "zielort",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class PersonAngabeForm(forms.ModelForm):
    class Meta:
        model = PersonAngabe
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PersonAngabeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class PersonLadungFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonLadungFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "person",
                    "ladung",
                    "person_an",
                    "person_einem_dem",
                    "person_per",
                    "person_pro_fur",
                    "person_zugeordnet",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class PersonLadungForm(forms.ModelForm):
    class Meta:
        model = PersonLadung
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PersonLadungForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class PersonenBezeichnungFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonenBezeichnungFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_py",
                    "bezeichnung",
                    "bemerkungen",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class PersonenBezeichnungForm(forms.ModelForm):
    class Meta:
        model = PersonenBezeichnung
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PersonenBezeichnungForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class RegionFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RegionFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup("Advanced search", "legacy_pk", "name", css_id="more"),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RegionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class ScanFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ScanFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "datei_name",
                    "ordner",
                    "phaidra_id",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ScanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class VorNameFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(VorNameFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search", "legacy_pk", "name", "bemerkungen", css_id="more"
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class VorNameForm(forms.ModelForm):
    class Meta:
        model = VorName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(VorNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class WareFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WareFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "name",
                    "beschreibung",
                    "name_orig",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class WareForm(forms.ModelForm):
    class Meta:
        model = Ware
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(WareForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class WareLadungFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WareLadungFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "id", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search",
                    "legacy_pk",
                    "ladung",
                    "ware",
                    "anzahl",
                    "anzahl_original",
                    "einheit",
                    "maut_fl",
                    "maut_s",
                    "maut_d",
                    "waren_order",
                    css_id="more",
                ),
                AccordionGroup("admin", "legacy_id", css_id="admin_search"),
            ),
        )


class WareLadungForm(forms.ModelForm):
    einheit = forms.ModelChoiceField(
        required=False,
        label="Einheit",
        queryset=SkosConcept.objects.filter(collection__name="einheit"),
    )

    class Meta:
        model = WareLadung
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(WareLadungForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )
