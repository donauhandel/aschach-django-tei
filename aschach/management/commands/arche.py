import os
from aschach.models import Angabe, Person, Ort
from django.core.management.base import BaseCommand
from rdflib import Graph, URIRef, RDF, Literal, XSD
from django.conf import settings

from archeutils.utils import acdh_ns as ARCHE
from archeutils.pids import PIDS


media = settings.MEDIA_ROOT
tei_out = os.path.join(media, "tei_out")
os.makedirs(tei_out, exist_ok=True)

SEED_FILE = "./aschach/arche.ttl"
BASE_URI = "https://id.acdh.oeaw.ac.at/donauhandel-aschach"


class Command(BaseCommand):
    # Show this when the user types help
    help = "create arche-md ttl"

    # A command must define handle()
    def handle(self, *args, **options):
        g = Graph()
        g.parse(SEED_FILE)
        register_item = URIRef(
            "https://id.acdh.oeaw.ac.at/donauhandel-aschach/listplace.xml"
        )
        g.add(
            (
                register_item,
                ARCHE["hasExtent"],
                Literal(f"{Ort.objects.all().count()} Ortseinträge", lang="de"),
            )
        )
        register_item = URIRef(
            "https://id.acdh.oeaw.ac.at/donauhandel-aschach/listperson.xml"
        )
        g.add(
            (
                register_item,
                ARCHE["hasExtent"],
                Literal(f"{Person.objects.all().count()} Personeneinträge", lang="de"),
            )
        )
        hs = set(
            [
                x
                for x in Angabe.objects.values_list(
                    "scan__ordner", flat=True
                ).distinct()
                if x is not None
            ]
        )
        for x in list(hs):
            items = Angabe.objects.filter(scan__ordner=x).distinct().order_by("datum")
            better_date = items.filter(datum__gt="1000-01-01").order_by("datum")
            datum = f"{better_date.first().datum}"
            last_year = f"{better_date.last().datum}"[:4]
            year = datum[:4]
            if datum.startswith('16'):
                continue
            print(x, datum, last_year)
            file_name = f"{x}.xml"
            subj = URIRef(f"{BASE_URI}/{file_name}")
            if last_year == year:
                title_str = f"Einträge Aschacher Mautprotokolle von {year}"
                description = f"XML/TEI Serialisierung von {items.count()} Einträgen in den Aschacher Mautprotokollen aus dem Jahr {year}."
            else:
                title_str = f"Einträge, Nachträge Aschacher Mautprotokolle von {year} bis {last_year}"
                description = f"XML/TEI Serialisierung von {items.count()} Einträgen in den Aschacher Mautprotokollen aus den Jahren {year} bis {last_year}."
            g.add((subj, RDF.type, ARCHE["Resource"]))
            g.add((subj, ARCHE["hasTitle"], Literal(title_str, lang="de")))
            g.add(
                (
                    subj,
                    ARCHE["hasExtent"],
                    Literal(f"{items.count()} Einträge", lang="de"),
                )
            )
            g.add((subj, ARCHE["hasDescription"], Literal(description, lang="de")))
            g.add(
                (
                    subj,
                    ARCHE["hasCoverageStartDate"],
                    Literal(f"{better_date.first().datum}", datatype=XSD.date),
                )
            )
            g.add(
                (
                    subj,
                    ARCHE["hasCoverageEndDate"],
                    Literal(f"{better_date.last().datum}", datatype=XSD.date),
                )
            )
            g.add(
                (
                    subj,
                    ARCHE["hasRightsHolder"],
                    URIRef("https://d-nb.info/gnd/13140007X"),
                )
            )
            g.add((subj, ARCHE["hasOwner"], URIRef("https://d-nb.info/gnd/13140007X")))
            g.add(
                (subj, ARCHE["hasLicensor"], URIRef("https://d-nb.info/gnd/13140007X"))
            )
            g.add(
                (
                    subj,
                    ARCHE["hasLicense"],
                    URIRef("https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0"),
                )
            )
            g.add((subj, ARCHE["isPartOf"], URIRef(BASE_URI)))
            g.add(
                (
                    subj,
                    ARCHE["hasMetadataCreator"],
                    URIRef("https://d-nb.info/gnd/1043833846"),
                )
            )
            g.add(
                (subj, ARCHE["hasDepositor"], URIRef("https://d-nb.info/gnd/13140007X"))
            )
            g.add(
                (
                    subj,
                    ARCHE["hasCategory"],
                    URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei"),
                )
            )
            # print(f"gathering data for {title_str}")
        for s in g.subjects(RDF.type, ARCHE["Resource"]):
            try:
                pid = PIDS[f"{s}"]
            except KeyError:
                print(f"no PID registered yet for {s}")
                continue
            g.add((
                s, ARCHE["hasPid"], Literal(pid)
            ))
        g.serialize(os.path.join(tei_out, "arche.ttl"))
        os.chmod(os.path.join(tei_out, "arche.ttl"), 0o777)
