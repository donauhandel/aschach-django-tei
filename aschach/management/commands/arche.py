import os
from aschach.models import Angabe
from django.core.management.base import BaseCommand
from rdflib import Graph, URIRef, RDF, Literal, XSD
from django.conf import settings

from archeutils.utils import acdh_ns as ARCHE


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

        hs = set([x for x in Angabe.objects.values_list('scan__ordner', flat=True).distinct() if x is not None])
        items = Angabe.objects.filter(related_person=None)
        for x in list(hs):
            items = Angabe.objects.filter(scan__ordner=x).distinct().order_by('datum')
            datum = f"{items.first().datum}"
            year = datum[:4]
            idno = x.replace("DepHarr_H", "")
            title_str = f"Aschacher Mautprotokoll {year} (Oberösterreichisches Landesarchiv, Depot Harrach, Handschrift {idno})"
            file_name = f"{x}.xml"
            subj = URIRef(f"{BASE_URI}/{file_name}")
            description = f"XML/TEI Serialisierung von {items.count()} Einträgen im Aschacher Mautprotokoll aus dem Jahr {year}."
            g.add((
                subj, RDF.type, ARCHE["Resource"]
            ))
            g.add((
                subj, ARCHE["hasTitle"], Literal(title_str, lang="de")
            ))
            g.add((
                subj, ARCHE["hasExtent"], Literal(f"{items.count()} Einträge", lang="de")
            ))
            g.add((
                subj, ARCHE["hasDescription"], Literal(description, lang="de")
            ))
            g.add((
                subj, ARCHE["hasCoverageStartDate"], Literal(f"{items.first().datum}", datatype=XSD.date)
            ))
            g.add((
                subj, ARCHE["hasCoverageEndDate"], Literal(f"{items.last().datum}", datatype=XSD.date)
            ))
            g.add((
                subj, ARCHE["hasRightsHolder"], URIRef("https://d-nb.info/gnd/13140007X")
            ))
            g.add((
                subj, ARCHE["hasOwner"], URIRef("https://d-nb.info/gnd/13140007X")
            ))
            g.add((
                subj, ARCHE["hasLicensor"], URIRef("https://d-nb.info/gnd/13140007X")
            ))
            g.add((
                subj, ARCHE["hasLicense"], URIRef("https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0")
            ))
            g.add((
                subj, ARCHE["isPartOf"], URIRef(BASE_URI)
            ))
            g.add((
                subj, ARCHE["hasMetadataCreator"], URIRef("https://d-nb.info/gnd/1043833846")
            ))
            g.add((
                subj, ARCHE["hasDepositor"], URIRef("https://d-nb.info/gnd/13140007X")
            ))
            g.add((
                subj, ARCHE["hasCategory"], URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei")
            ))
            print(f"gathering data for {title_str}")
        g.serialize(os.path.join(tei_out, "arche.ttl"))
