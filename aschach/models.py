import lxml.etree as ET

from dateutil.parser import parse
from babel.dates import format_date
from next_prev import next_in_order, prev_in_order
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from vocabs.models import SkosConcept
from browsing.browsing_utils import model_to_dict
from tei.archiv_utils import MakeTeiDoc

from aschach.skosify import skosify_ware_from_template
from archeutils.utils import as_arche_graph


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra


class Uri(models.Model):
    """Beschreibt einen Normdateneintrag"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    uri = models.CharField(max_length=300, blank=True, verbose_name="Normdata URL")
    domain = models.CharField(max_length=300, blank=True, verbose_name="Normdatequelle")

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Normdaten URL"

    def __str__(self):
        if self.uri is not None:
            return f"{self.uri}"
        else:
            return f"{self.id}"


class SchiffTyp(models.Model):
    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personenId",
    )
    fahrzeug = models.ForeignKey(
        "Fahrzeug",
        related_name="rvn_fahrzeug_anzahl",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fahrzeug",
        help_text="Fahrzeug",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeugId",
    )
    skosconcept = models.ForeignKey(
        SkosConcept,
        related_name="rvn_fahrzeugtyp_von",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fahrzeugtyp",
        help_text="Fahrzeugtyp",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeugTyp",
    )
    anzahl = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Anzahl",
        help_text="Anzahl",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeugAnzahl",
    )
    leer = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="leer",
        help_text="leer",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_anzahlTyp_leer___fahrzeug_anzahlTypId___leer",
    )
    geschirr = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="geschirr",
        help_text="geschirr",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_anzahlTyp_mitGeschirr___fahrzeug_anzahlTypId___mitGeschirr",
    )
    rossen = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="rossen",
        help_text="rossen",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_anzahlTyp_mitRossen___fahrzeug_anzahlTypId___mitRossen",
    )
    mit_sg = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="mit_sg",
        help_text="mit_sg",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_anzahlTyp_mitSG___fahrzeug_anzahlTypId___mitSG",
    )
    mit_sich_selbst = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="mit_sich_selbst",
        help_text="mit_sich_selbst",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_anzahlTyp_mitSichSelbst___fahrzeug_anzahlTypId___mitSG",
    )

    def __str__(self):
        return f"{self.skosconcept} ({self.anzahl})"


class Fahrzeug(models.Model):
    """Fahrzeug"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="fahrzeugId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    person = models.ForeignKey(
        "Person",
        related_name="rvn_fahrzeug_person_person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Personen",
        help_text="Personen",
    ).set_extra(
        is_public=True,
        data_lookup="personenId",
    )
    herkunft = models.ForeignKey(
        "Ort",
        related_name="rvn_fahrzeug_herkunft_ort",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Herkunftsort",
        help_text="Herkunftsort",
    ).set_extra(
        is_public=True,
        data_lookup="herkunft",
    )
    region = models.ForeignKey(
        "Region",
        related_name="rvn_fahrzeug_region_ort",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Region",
        help_text="Region",
    ).set_extra(
        is_public=True,
        data_lookup="region",
    )
    fahrtrichtung = models.ForeignKey(
        SkosConcept,
        related_name="rvn_fahrzeug_fahrtrichtung_skosconcept",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fahrtrichtung",
        help_text="Fahrtrichtung",
    ).set_extra(
        is_public=True,
        data_lookup="fahrtrichtungId",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_bemerkungen___fahrzeugId___bemerkung#Property",
        arche_prop="hasNote",
    )
    anzahl_pferde = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Anzahl der Pferde",
        help_text="Anzahl der Pferde",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_fahrtrichtung_pferde___fahrzeugId___anzahlPferde#Property",
    )
    hohenau = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Hohenau",
        help_text="Hohenau",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_hohenau___fahrzeugId___hohenau#Property",
    )
    zielort = models.ForeignKey(
        "Ort",
        related_name="rvn_fahrzeug_zielort_ort",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Zielort",
        help_text="Zielort",
    ).set_extra(
        is_public=True,
    )
    zurueck = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="zurück",
        help_text="zurück",
    ).set_extra(
        is_public=True,
        data_lookup="fahrzeuge_zurueck___fahrzeugId___zurueck#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)
    schiff_typ = models.ManyToManyField(
        SkosConcept,
        through="SchiffTyp",
        related_name="rvn_schifftyp",
        blank=True,
        verbose_name="Personen",
        help_text="Personen",
    )

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Fahrzeug"

    def __str__(self):
        if self.id:
            return "{}".format(self.id)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:fahrzeug_browse")

    @classmethod
    def get_source_table(self):
        return "fahrzeuge"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:fahrzeug_create")

    def get_schifftyp(self):
        return SchiffTyp.objects.filter(fahrzeug=self)

    def get_absolute_url(self):
        return reverse("aschach:fahrzeug_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:fahrzeug_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:fahrzeug_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Firma(models.Model):
    """Firma"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="firmenId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Firmenname",
        help_text="Firmenname",
    ).set_extra(
        is_public=True,
        data_lookup="firma",
        arche_prop="hasTitle",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="firmen_bemerkungen___firmenId___bemerkung#Property",
    )
    name_orig = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Name (originale Schreibweise)",
        help_text="Name (originale Schreibweise)",
    ).set_extra(
        is_public=True,
        data_lookup="firmen_quelle___firmenId___firmaQuelle#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name = "Firma"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:firma_browse")

    @classmethod
    def get_source_table(self):
        return "firmen"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:firma_create")

    def get_absolute_url(self):
        return reverse("aschach:firma_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:firma_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:firma_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class MengeGebinde(models.Model):
    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="ladung_warenId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    ladung = models.ForeignKey(
        "Ladung",
        related_name="rvn_ladung_menge",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ladung",
        help_text="Ladung",
    ).set_extra(
        is_public=True,
        data_lookup="ladungId",
    )
    menge = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name="Menge der Wareneingebinden",
        help_text="Menge der Wareneingebinden",
    ).set_extra(
        is_public=True,
        data_lookup="menge",
    )
    gebinde = models.ForeignKey(
        SkosConcept,
        related_name="rvn_ladungmenge_einheit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Gebinde",
        help_text="Gebinde",
    ).set_extra(
        is_public=True,
        data_lookup="gebinde",
    )

    @classmethod
    def get_source_table(self):
        return "ladung_mengeVerpackung"

    def __str__(self):
        return f"{self.menge} {self.gebinde}"


class Ladung(models.Model):
    """Ladung"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="ladungId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_bemerkungen___ladungId___bemerkung#Property",
        arche_prop="hasNote",
    )
    dreilingsgeld = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Dreilingsgeld",
        help_text="Dreilingsgeld",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_dreilingsgeld___ladungId___dreilingsgeld#Property",
    )
    kammergut = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Kammergut",
        help_text="Kammergut",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_kammergut___ladungId___kammergut#Property",
    )
    mautbefreiung = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Mautbefreiung",
        help_text="Mautbefreiung",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_mautbefreiung___ladungId___mautbefreiung#Property",
    )
    mautbefreiung_all = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Mautbefreiung (alle)",
        help_text="Mautbefreiung",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_mautbefreiungAll___ladungId___mautbefreiungAll#Property",
    )
    niederlage = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Niederlage",
        help_text="Niederlage",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_niederlage___ladungId___niederlage#Property",
    )
    passbrief = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Passbrief",
        help_text="Passbrief",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_passbrief___ladungId___passbrief#Property",
    )
    per_kommission = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Per Kommission",
        help_text="Per Kommission",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_perKommission___ladungId___perKommission#Property",
    )
    per_schiffmeister = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Per Schiffmeister",
        help_text="Per Schiffmeister",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_perSchiffmeister___ladungId___perSchiffmeister#Property",
    )
    per_schiffukgut = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Per Schiff UKGut",
        help_text="Per Schiff UKGut",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_perSchiffUKGut___ladungId___perSchiffUKGut#Property",
    )
    personen = models.ManyToManyField(
        "Person",
        through="PersonLadung",
        related_name="rvn_fahrzeug_zielort_ort",
        blank=True,
        verbose_name="Personen",
        help_text="Personen",
    ).set_extra(
        is_public=True,
    )
    waren = models.ManyToManyField(
        "Ware",
        through="WareLadung",
        related_name="rvn_fahrzeug_zielort_ort",
        blank=True,
        verbose_name="Waren",
        help_text="Waren",
    ).set_extra(
        is_public=True,
    )
    weitertransport = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Weitertransport der Waren",
        help_text="Weitertransport der Ware",
    ).set_extra(
        is_public=True,
        data_lookup="weitertransport",
    )
    zielort = models.ManyToManyField(
        "Ort",
        related_name="rvn_ladung_zielort_ort",
        blank=True,
        verbose_name="Zielort der Ladung",
        help_text="Zielort der Ladung",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_zielort___ladungId___zielort",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)
    menge_gebinde = models.ManyToManyField(
        MengeGebinde,
        related_name="rvn_ladung_menge_gebinde",
        blank=True,
        verbose_name="Menge",
        help_text="Anzahl/Zusammensetzung der Waren",
    )

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Ladung"

    def __str__(self):
        if self.id:
            return "{}".format(self.id)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:ladung_browse")

    @classmethod
    def get_source_table(self):
        return "ladung"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:ladung_create")

    def get_absolute_url(self):
        return reverse("aschach:ladung_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:ladung_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:ladung_edit", kwargs={"pk": self.id})

    @cached_property
    def get_wl(self):
        wl = []
        for y in WareLadung.objects.filter(ladung=self.id):
            wl.append(
                {
                    "ladung": self,
                    "warenladung": y,
                    "personenLadung": PersonLadung.objects.filter(ladung=self.id),
                }
            )
        return wl

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class NachName(models.Model):
    """Nachname"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Nachname",
        help_text="Nachname",
    ).set_extra(
        is_public=True,
        data_lookup="nachname",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="nachnamen_bemerkungen___nachnameId___bemerkung#Property",
    )
    name_orig = models.TextField(
        blank=True,
        null=True,
        verbose_name="Nachname (original)",
        help_text="Nachname (original)",
    ).set_extra(
        is_public=True,
        data_lookup="nachnamen_quelle___nachnameId___quelle#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name = "Nachname"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:nachname_browse")

    @classmethod
    def get_source_table(self):
        return "nachnamen"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:nachname_create")

    def get_absolute_url(self):
        return reverse("aschach:nachname_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:nachname_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:nachname_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Ort(models.Model):
    """Ort"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="herkunftId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    normdata_url = models.ManyToManyField(
        "Uri",
        related_name="rvn_defines_place",
        blank=True,
        verbose_name="Normdaten URL",
        help_text="Normdaten URL",
    ).set_extra(is_public=True, arche_prop="hasIdentifier")
    donau_normid = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Donau Norm (Krems) ID",
        help_text="Donau Norm (Krems) ID",
    ).set_extra(
        is_public=False,
        data_lookup="herkunftId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Donau Norm (Krems) ID: <value>",
    )
    lat = models.DecimalField(
        max_digits=19,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name="Breite",
        help_text="Breite (dezimal)",
    ).set_extra(
        is_public=True,
    )
    lng = models.DecimalField(
        max_digits=19,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name="Länge",
        help_text="Länge (dezimal)",
    ).set_extra(
        is_public=True,
    )
    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Ortsname",
        help_text="Ortsname",
    ).set_extra(
        is_public=True,
        data_lookup="herkunft",
        arche_prop="hasTitle",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="herkunft_bemerkungen___herkunftId___bemerkung#Property",
    )
    literatur = models.TextField(
        blank=True,
        null=True,
        verbose_name="Literatur",
        help_text="Literatur",
    ).set_extra(
        is_public=True,
        data_lookup="herkunft_literatur___herkunftId___literatur#Property",
    )
    name_orig = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Name (originale Schreibweise)",
        help_text="Name (originale Schreibweise)",
    ).set_extra(
        is_public=True,
        data_lookup="herkunft_quelle___herkunftId___quelle#Property",
    )
    region = models.ForeignKey(
        "Region",
        related_name="rvn_ort_region_region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Region",
        help_text="Region",
    ).set_extra(
        is_public=True,
        data_lookup="herkunft_region___herkunftId___region#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name = "Ort"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:ort_browse")

    @classmethod
    def get_source_table(self):
        return "herkunft"

    @classmethod
    def get_natural_primary_key(self):
        return "name"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:ort_create")

    def get_absolute_url(self):
        return reverse("aschach:ort_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:ort_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:ort_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Person(models.Model):
    """Person"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="personenId",
    )
    donau_normid = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Donau Norm (Krems) ID",
        help_text="Donau Norm (Krems) ID",
    ).set_extra(
        is_public=False,
        data_lookup="herkunftId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Donau Norm (Krems) ID: <value>",
    )
    normdata_url = models.ManyToManyField(
        "Uri",
        related_name="rvn_defines_person",
        blank=True,
        verbose_name="Normdaten URL",
        help_text="Normdaten URL",
    ).set_extra(is_public=True, arche_prop="hasIdentifier")
    has_title = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Name",
    ).set_extra(
        is_public=True,
        arche_prop="hasTitle",
    )
    nachname = models.ForeignKey(
        "NachName",
        related_name="rvn_person_nachname_nachname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Nachname",
        help_text="Nachname",
    ).set_extra(
        is_public=True,
        data_lookup="nachname",
    )
    vorname = models.ForeignKey(
        "VorName",
        related_name="rvn_person_vorname_vorname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Vorname",
        help_text="Vorname",
    ).set_extra(
        is_public=True,
        data_lookup="vorname",
    )
    firma = models.ForeignKey(
        "Firma",
        related_name="rvn_person_firma_firma",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Firma",
        help_text="Firma",
    ).set_extra(
        is_public=True,
        data_lookup="firma",
    )
    bezeichnung = models.ForeignKey(
        "PersonenBezeichnung",
        related_name="rvn_person_bezeichnung_personenbezeichnung",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Bezeichnung",
        help_text="Bezeichnung",
    ).set_extra(
        is_public=True,
        data_lookup="personenBezeichnung",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="personen_bemerkungen___personenId___bemerkung#Property",
    )
    weiblich = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="weiblich",
        help_text="weiblich",
    ).set_extra(
        is_public=True,
        data_lookup="personen_frau___personenId___frau#Property",
    )
    herkunft = models.ForeignKey(
        "Ort",
        related_name="rvn_person_herkunft_ort",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Herkunftsort",
        help_text="Herkunftsort",
    ).set_extra(
        is_public=True,
        data_lookup="personen_herkunft___personenId___herkunft",
    )
    jude = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="jüdisch",
        help_text="jüdisch",
    ).set_extra(
        is_public=True,
        data_lookup="personen_jude___personenId___jude#Property",
    )
    verknuepft = models.ManyToManyField(
        "Person",
        related_name="rvn_person_verknuepft_person",
        blank=True,
        verbose_name="verknüpft",
        help_text="verknüpft",
    ).set_extra(
        is_public=True,
        data_lookup="personen_verknuepft___personenId1___personenId2",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Person"

    def __str__(self):
        return f"{self.has_title} (id: {self.id})"

    def save(self, *args, **kwargs):
        name_parts = []
        if self.nachname is not None:
            name_parts.append(self.nachname.name)
        if self.vorname is not None:
            name_parts.append(self.vorname.name)
        if self.firma is not None:
            name_parts.append(f"{self.firma.name} (Firma)")
        if len(name_parts) > 0:
            self.has_title = ", ".join(name_parts)
        else:
            self.has_title = "N.N."
        super(Person, self).save(*args, **kwargs)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:person_browse")

    @classmethod
    def get_source_table(self):
        return "personen"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:person_create")

    def get_absolute_url(self):
        return reverse("aschach:person_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:person_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:person_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class PersonAngabe(models.Model):
    """PersonAngabe"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_passagiereId",
    )
    person = models.ForeignKey(
        "Person",
        related_name="rvn_personangabe_person_person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Person",
        help_text="Person",
    ).set_extra(
        is_public=True,
        data_lookup="personenId",
    )
    angabe = models.ForeignKey(
        "Angabe",
        related_name="rvn_personangabe_angabe_angabe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Angabe",
        help_text="Angabe",
    ).set_extra(
        is_public=True,
        data_lookup="angabenId",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="passagiere_bemerkungen___angaben_passagiereId___bemerkungen#Property",
    )
    judenleibmaut = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Judenleibmaut",
        help_text="Judenleibmaut",
    ).set_extra(
        is_public=True,
        data_lookup="passagiere_judenleibmaut___angaben_passagiereId___judenleibmaut#Property",
    )
    judenleibmaut_fl = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Judenleibmaut (Gulden)",
        help_text="Judenleibmaut (Gulden)",
    ).set_extra(
        is_public=True,
        data_lookup="passagiere_judenleibmaut___angaben_passagiereId___judenleibmaut_fl#Property",
    )
    judenleibmaut_s = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Judenleibmaut (Schilling)",
        help_text="Judenleibmaut (Schilling)",
    ).set_extra(
        is_public=True,
        data_lookup="passagiere_judenleibmaut___angaben_passagiereId___judenleibmaut_s#Property",
    )
    judenleibmaut_d = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Judenleibmaut (d)",
        help_text="Judenleibmaut (d)",
    ).set_extra(
        is_public=True,
        data_lookup="passagiere_judenleibmaut___angaben_passagiereId___judenleibmaut_d#Property",
    )
    zielort = models.ForeignKey(
        "Ort",
        related_name="rvn_personangabe_zielort_ort",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Zielort Passagier",
        help_text="Zielort Passagier",
    ).set_extra(
        is_public=True,
        data_lookup="passagiere_zielort___angaben_passagiereId___zielort#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "PersonAngabe"

    def __str__(self):
        if self.id:
            return "{}".format(self.id)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:personangabe_browse")

    @classmethod
    def get_source_table(self):
        return "angaben_passagiere"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:personangabe_create")

    def get_absolute_url(self):
        return reverse("aschach:personangabe_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:personangabe_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:personangabe_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class PersonLadung(models.Model):
    """PersonLadung"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personenId",
    )
    person = models.ForeignKey(
        "Person",
        related_name="rvn_personladung_person_person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Person",
        help_text="Person",
    ).set_extra(
        is_public=True,
        data_lookup="personenId",
    )
    ladung = models.ForeignKey(
        "Ladung",
        related_name="rvn_personladung_ladung_ladung",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ladung",
        help_text="Ladung",
    ).set_extra(
        is_public=True,
        data_lookup="ladungId",
    )
    person_an = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Person (an)",
        help_text="Person (an)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personen_an___ladung_personenId___an#Property",
    )
    person_einem_dem = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Person (einemDem)",
        help_text="Person (einemDem)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personen_einemDem___ladung_personenId___einemDem#Property",
    )
    person_per = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Person (per)",
        help_text="Person (per)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personen_per___ladung_personenId___per#Property",
    )
    person_pro_fur = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Person (pro Für)",
        help_text="Person (pro Für)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personen_proFuer___ladung_personenId___proFuer#Property",
    )
    person_zugeordnet = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Person (zugeordnet)",
        help_text="Person (zugeordnet)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_personen_zugeordnet___ladung_personenId___zugeordnet#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "PersonLadung"

    def __str__(self):
        if self.id:
            return "{}".format(self.id)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:personladung_browse")

    @classmethod
    def get_source_table(self):
        return "ladung_personen"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:personladung_create")

    def get_absolute_url(self):
        return reverse("aschach:personladung_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:personladung_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:personladung_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class PersonenBezeichnung(models.Model):
    """Personenbezeichnung"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_py = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="personenBezeichnungId",
    )
    bezeichnung = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Bezeichnung",
        help_text="Bezeichnung",
    ).set_extra(
        is_public=True,
        data_lookup="bezeichnung",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="personenBezeichnung_bemerkungen___personenBezeichnungId___bemerkung#Property",
        arche_prop="hasNote",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Personenbezeichnung"

    def __str__(self):
        if self.bezeichnung:
            return "{}".format(self.bezeichnung)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:personenbezeichnung_browse")

    @classmethod
    def get_source_table(self):
        return "personenBezeichnung"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:personenbezeichnung_create")

    def get_absolute_url(self):
        return reverse("aschach:personenbezeichnung_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:personenbezeichnung_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:personenbezeichnung_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Region(models.Model):
    """Region"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="regionId",
    )
    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Name",
        help_text="Name",
    ).set_extra(
        is_public=True,
        data_lookup="region",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name = "Region"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:region_browse")

    @classmethod
    def get_source_table(self):
        return "regionen"

    @classmethod
    def get_natural_primary_key(self):
        return "name"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:region_create")

    def get_absolute_url(self):
        return reverse("aschach:region_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:region_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:region_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Scan(models.Model):
    """Scan"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="scanId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    datei_name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Dateiname",
        help_text="Dateiname",
    ).set_extra(
        is_public=True,
        data_lookup="datei",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Dateiname: <value>",
    )
    ordner = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Ordner",
        help_text="Ordner",
    ).set_extra(
        is_public=True,
        data_lookup="ordner",
    )
    phaidra_id = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Phaidra ID",
        help_text="Phaidra ID",
    ).set_extra(
        is_public=True,
        data_lookup="phaidra",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Phaidra ID: <value>",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "datei_name",
        ]
        verbose_name = "Scan"

    def __str__(self):
        if self.datei_name:
            return "{}".format(self.datei_name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:scan_browse")

    @classmethod
    def get_source_table(self):
        return "scans"

    @classmethod
    def get_natural_primary_key(self):
        return "datei_name"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:scan_create")

    def get_absolute_url(self):
        return reverse("aschach:scan_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:scan_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:scan_edit", kwargs={"pk": self.id})

    def get_hs(self):
        if "_" in self.datei_name:
            hs = self.datei_name.split("_")[0]
        else:
            hs = "Hs999"
        return f"{hs[1:]}"

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class VorName(models.Model):
    """Vorname"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="vornameId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Vorname",
        help_text="Vorname",
    ).set_extra(
        is_public=True,
        data_lookup="vorname",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="vornamen_bemerkungen___vornameId___bemerkungen#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name = "Vorname"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:vorname_browse")

    @classmethod
    def get_source_table(self):
        return "vornamen"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:vorname_create")

    def get_absolute_url(self):
        return reverse("aschach:vorname_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:vorname_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:vorname_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Ware(models.Model):
    """Ware"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="warenId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Ware",
        help_text="Ware",
    ).set_extra(
        is_public=True,
        data_lookup="ware",
        arche_prop="hasTitle",
    )
    beschreibung = models.TextField(
        blank=True,
        null=True,
        verbose_name="Kurzbeschreibung",
        help_text="Kurzbeschreibung",
    ).set_extra(
        is_public=True,
        data_lookup="waren_kurzbeschreibung___warenId___kurzbeschreibung#Property",
        arche_prop="hasNote",
    )
    name_orig = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ware (originale Schreibweise)",
        help_text="Ware (originale Schreibweise)",
    ).set_extra(
        is_public=True,
        data_lookup="waren_quelle___warenId___quelle#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Ware"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:ware_browse")

    @classmethod
    def get_source_table(self):
        return "waren"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:ware_create")

    def as_skos(self):
        return skosify_ware_from_template(self, "aschach/skosify_ware.xml")

    def get_absolute_url(self):
        return reverse("aschach:ware_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:ware_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:ware_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class WareLadung(models.Model):
    """WareLadung"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_warenId",
    )
    ladung = models.ForeignKey(
        "Ladung",
        related_name="rvn_wareladung_ladung_ladung",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ladung",
        help_text="Ladung",
    ).set_extra(
        is_public=True,
        data_lookup="ladungId",
    )
    ware = models.ForeignKey(
        "Ware",
        related_name="rvn_wareladung_ware_ware",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ware",
        help_text="Ware",
    ).set_extra(
        is_public=True,
        data_lookup="warenId",
    )
    anzahl = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Anzahl",
        help_text="Anzahl",
    ).set_extra(
        is_public=True,
        data_lookup="anzahl",
    )
    anzahl_original = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Anzahl (original)",
        help_text="Anzahl (original)",
    ).set_extra(
        is_public=True,
        data_lookup="anzahlWoertlich",
    )
    einheit = models.ForeignKey(
        SkosConcept,
        related_name="rvn_wareladung_einheit_skosconcept",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Einheit",
        help_text="Einheit",
    ).set_extra(
        is_public=True,
        data_lookup="einheit",
    )
    maut_fl = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Maut (Gulden)",
        help_text="Maut (Gulden)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_waren_maut___ladung_warenId___maut_fl#Property",
    )
    maut_s = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Maut (Schilling)",
        help_text="Maut (Schilling)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_waren_maut___ladung_warenId___maut_s#Property",
    )
    maut_d = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Maut (d)",
        help_text="Maut (d)",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_waren_maut___ladung_warenId___maut_d#Property",
    )
    waren_order = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="warenOrder",
        help_text="warenOrder",
    ).set_extra(
        is_public=True,
        data_lookup="ladung_waren_warenOrder___ladung_warenId___warenOrder#Property",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "WareLadung"

    def __str__(self):
        if self.id:
            return "{}".format(self.id)
        else:
            return "{}".format(self.legacy_id)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:wareladung_browse")

    @classmethod
    def get_source_table(self):
        return "ladung_waren"

    @classmethod
    def get_natural_primary_key(self):
        return "id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:wareladung_create")

    def get_absolute_url(self):
        return reverse("aschach:wareladung_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:wareladung_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:wareladung_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False


class Angabe(models.Model):
    """Beschreibt eine Angabe"""

    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    legacy_pk = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Primärschlüssel Alt",
        help_text="Primärschlüssel Alt",
    ).set_extra(
        is_public=False,
        data_lookup="angabenId",
        arche_prop="hasNonLinkedIdentifier",
        arche_prop_str_template="Primärschlüssel Alt: <value>",
    )
    datum_original = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Datum (als Text)",
        help_text="Datum (als Text)",
    ).set_extra(
        is_public=True,
        data_lookup="datum",
    )
    datum = models.DateField(
        blank=True,
        null=True,
        verbose_name="Datum",
        help_text="Datum",
    ).set_extra(
        is_public=True,
        arche_prop="hasCoverageStartDate",
    )
    quelle = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Quelle",
        help_text="Quelle",
    ).set_extra(
        is_public=True,
        data_lookup="quelle",
    )
    bildnummern = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Bildnummern",
        help_text="Bildnummern",
    ).set_extra(
        is_public=True,
        data_lookup="bildnummer",
    )
    bemerkungen = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bemerkungen",
        help_text="Bemerkungen",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_bemerkungen___angabenId___bemerkungen#Property",
        arche_prop="hasNote",
    )
    eiskalt = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Eiskalt",
        help_text="Eiskalt",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_eisKalt___angabenId___eisKalt#Property",
    )
    fahrzeug = models.ManyToManyField(
        "Fahrzeug",
        related_name="rvn_angabe_fahrzeug_fahrzeug",
        blank=True,
        verbose_name="Fahrzeuge",
        help_text="Fahrzeuge",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_fahrzeug___angabenId___fahrzeugId",
    )
    hochwasser = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Hochwasser",
        help_text="Hochwasser",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_hochwasser___angabenId___hochwasser#Property",
    )
    ladung = models.ManyToManyField(
        "Ladung",
        related_name="rvn_angabe_ladung_ladung",
        blank=True,
        verbose_name="Ladung",
        help_text="Ladung",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_ladung___angabenId___ladungId",
    )
    nichts = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Nichts",
        help_text="Nichts",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_nichts___angabenId___nichts#Property",
    )
    passagiere = models.ManyToManyField(
        "Person",
        through="PersonAngabe",
        related_name="rvn_angabe_ladung_ladung",
        blank=True,
        verbose_name="Passagiere",
        help_text="Passagiere",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_passagiere___personenId___angabenId",
    )
    scan = models.ManyToManyField(
        "Scan",
        related_name="rvn_angabe_scan_scan",
        blank=True,
        verbose_name="Scan",
        help_text="Scan",
    ).set_extra(
        is_public=True,
        data_lookup="angaben_scans___angabenId___scanId",
    )
    orig_data_csv = models.TextField(
        blank=True, null=True, verbose_name="The original data"
    ).set_extra(is_public=True)

    related_good = models.ManyToManyField(
        "Ware",
        blank=True,
        verbose_name="Waren",
        related_name="mentioned_in_Angabe",
        help_text="Auflistung der genannten Waren",
    )
    related_person = models.ManyToManyField(
        "Person",
        blank=True,
        related_name="mentioned_in_Angabe",
        verbose_name="Person",
        help_text="Auflistung der genannten Personen",
    )
    related_place = models.ManyToManyField(
        "Ort",
        blank=True,
        verbose_name="Ort",
        related_name="mentioned_in_Angabe",
        help_text="Auflistung der genannten Ort",
    )

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Angabe"

    @cached_property
    def get_idno(self):
        try:
            idno = f"{self.scan.values_list('datei_name')[0]}".split("_")[0][2:]
        except:
            idno = "Hs999"
        return idno

    def __str__(self):
        if self.id:
            return f"{self.get_idno}, S. {self.bildnummern}, ID {self.legacy_pk}"
        else:
            return "{}".format(self.legacy_id)

    def save(self, *args, **kwargs):
        date_str = self.datum_original
        try:
            date_obj = parse(date_str)
        except:
            date_obj = parse("1000-01-01")
        self.datum = date_obj
        super(Angabe, self).save(*args, **kwargs)

    def as_tei_class(self, full=True):
        return MakeTeiDoc(self, full=full)

    def as_arche(self):
        return as_arche_graph(self)

    def as_tei_node(self, full=True):
        my_node = MakeTeiDoc(self, full=full)
        return my_node.export_full_doc(full=full)

    def as_tei(self, full=True):
        return ET.tostring(self.as_tei_node(full=full), pretty_print=True, encoding="UTF-8")

    def date_german(self):
        return format_date(self.datum, locale="de_DE", format="full")

    def get_formatted_nr(self):
        return f"{self.legacy_pk:06}"

    def facs_in_phaidra(self):
        ph_ids = [x.phaidra_id for x in self.scan.all()]
        if len(ph_ids) > 0:
            return ph_ids
        else:
            return False

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse("aschach:angabe_browse")

    def get_tei_url(self):
        return reverse("aschach:angabe_xml_tei", kwargs={"pk": self.id})

    @classmethod
    def get_source_table(self):
        return "angaben"

    @classmethod
    def get_natural_primary_key(self):
        return "legacy_id"

    @classmethod
    def get_createview_url(self):
        return reverse("aschach:angabe_create")

    @cached_property
    def get_wl(self):
        wl = []
        for x in self.ladung.all():
            for y in WareLadung.objects.filter(ladung=x.id):
                wl.append(
                    {
                        "ladung": x,
                        "warenladung": y,
                        "personenLadung": PersonLadung.objects.filter(ladung=x.id),
                    }
                )
        return wl

    @cached_property
    def get_waren_einheiten(self):
        waren = []
        einheiten = []
        for x in self.get_wl:
            if not x["warenladung"].ware in waren:
                waren.append(x["warenladung"].ware)
            if (
                not x["warenladung"].einheit in einheiten and x["warenladung"].einheit is not None
            ):
                einheiten.append(x["warenladung"].einheit)
        return {"waren": waren, "einheiten": einheiten}

    @cached_property
    def get_persons(self):
        personen = []
        for x in self.passagiere.all():
            if x not in personen:
                personen.append(x)
        for x in self.get_wl:
            try:
                x = x["personenLadung"][0].person
            except IndexError:
                continue
            if x not in personen:
                personen.append(x)
        for x in self.fahrzeug.all():
            if x.person not in personen:
                personen.append(x.person)
        personen = [x for x in personen if x is not None]
        return personen

    @cached_property
    def get_places(self):
        places = []
        for x in self.fahrzeug.all():
            if x.herkunft not in places:
                places.append(x.herkunft)
            if x.zielort not in places:
                places.append(x.zielort)
        for x in self.ladung.all():
            for y in x.zielort.all():
                if y not in places:
                    places.append(y)
        for x in self.get_wl:
            try:
                x = x["personenLadung"][0].person
            except IndexError:
                continue
            try:
                if x.herkunft not in places:
                    places.append(x.herkunft)
            except AttributeError:
                continue
        places = [x for x in places if x is not None]
        return places

    def get_waren(self):
        ladungen = self.ladung.all()
        wl = WareLadung.objects.filter(ladung__in=ladungen)
        waren = Ware.objects.filter(rvn_wareladung_ware_ware__in=wl).distinct()
        return waren

    def get_absolute_url(self):
        return reverse("aschach:angabe_detail", kwargs={"pk": self.id})

    def get_arche_url(self):
        return reverse("aschach:angabe_arche", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("aschach:angabe_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("aschach:angabe_edit", kwargs={"pk": self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.get_absolute_url()
        return False

    def get_next_obj(self):
        next = next_in_order(self)
        if next:
            return next.id
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.get_absolute_url()
        return False

    def get_prev_obj(self):
        prev = prev_in_order(self)
        if prev:
            return prev.id
        return False
