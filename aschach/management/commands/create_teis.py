import os
import shutil
from tqdm import tqdm
import lxml.etree as ET

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader

from aschach.models import Angabe, Person, Ort
from tei.persons import TeiPerson
from tei.places import TeiPlace


class Command(BaseCommand):
    # Show this when the user types help
    help = "serializes Angaben as TEI-Files"

    # A command must define handle()
    def handle(self, *args, **options):
        media = settings.MEDIA_ROOT
        tei_out = os.path.join(media, "tei_out")
        shutil.rmtree(tei_out, ignore_errors=True)
        os.makedirs(tei_out, exist_ok=True)
        items = Person.objects.all()
        # persons
        template = loader.select_template(["tei/listperson.j2"])
        print(f"serializing {items.count()} Persons")
        file_name = "listperson.xml"
        context = {
            "file_name": file_name,
            "title": "Personenregister",
            "items": [],
        }
        for x in tqdm(items, total=items.count()):
            doc = TeiPerson(x).get_el()
            doc_str = ET.tostring(doc, encoding="utf-8").decode("utf-8")
            context["items"].append(doc_str)
        data = template.render(context)
        data = data.replace("ns0:", "")
        data = data.replace('xmlns:ns0="http://www.tei-c.org/ns/1.0"', "")
        data = data.replace("<person  xml", "<person xml")
        with open(os.path.join(tei_out, file_name), "w") as f:
            f.write(data)

        # places
        items = Ort.objects.all()
        template = loader.select_template(["tei/listperson.j2"])
        print(f"serializing {items.count()} Orte")
        file_name = "listplace.xml"
        context = {
            "file_name": file_name,
            "title": "Ortsregister",
            "items": [],
        }
        for x in tqdm(items, total=items.count()):
            doc = TeiPlace(x).get_el()
            doc_str = ET.tostring(doc, encoding="utf-8").decode("utf-8")
            context["items"].append(doc_str)
        data = template.render(context)
        data = data.replace("ns0:", "")
        data = data.replace('xmlns:ns0="http://www.tei-c.org/ns/1.0"', "")
        data = data.replace("<place  xml", "<place xml")
        with open(os.path.join(tei_out, file_name), "w") as f:
            f.write(data)

        print("and now, let's serialize Angaben")
        template = loader.select_template(["tei/corpus.j2"])
        hs = set(
            [
                x
                for x in Angabe.objects.values_list(
                    "scan__ordner", flat=True
                ).distinct()
                if x is not None
            ]
        )
        items = Angabe.objects.filter(related_person=None)
        for x in list(hs):
            file_path = os.path.join(tei_out, f"{x}.xml")
            items = Angabe.objects.filter(scan__ordner=x).distinct().order_by("datum")
            better_date = items.filter(datum__gt="1000-01-01").order_by('datum')
            datum = f"{better_date.first().datum}"
            datum = f"{items.first().datum}"
            year = datum[:4]
            idno = x.replace("DepHarr_H", "")
            title_str = f"Aschacher Mautprotokoll {year} (Oberösterreichisches Landesarchiv, Depot Harrach, Handschrift {idno})"
            context = {
                "title": title_str,
                "year": year,
                "file_name": f"{x}.xml",
                "items": items.count(),
                "from": f"{items.first().datum}",
                "to": f"{items.last().datum}",
                "idno": idno,
                "teis": [],
            }
            print(f"gathering data for {title_str}")
            for item in tqdm(items, total=items.count()):
                context["teis"].append(item.as_tei(full=False).decode("utf-8"))
            context["item_count"] = len(context["teis"])
            print(f"writing {context['item_count']} items into {file_path}")
            with open(file_path, "w") as f:
                f.write(template.render(context))
