import os
import shutil
from tqdm import tqdm
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader

from aschach.models import Angabe


class Command(BaseCommand):
    # Show this when the user types help
    help = "serializes Angaben as TEI-Files"

    # A command must define handle()
    def handle(self, *args, **options):
        media = settings.MEDIA_ROOT
        tei_out = os.path.join(media, "tei_out")
        shutil.rmtree(tei_out, ignore_errors=True)
        os.makedirs(tei_out, exist_ok=True)
        template = loader.select_template(["tei/corpus.j2"])
        hs = set([x for x in Angabe.objects.values_list('scan__ordner', flat=True).distinct() if x is not None])
        items = Angabe.objects.filter(related_person=None)
        for x in list(hs):
            file_path = os.path.join(tei_out, f"{x}.xml")
            items = Angabe.objects.filter(scan__ordner=x).distinct().order_by('datum')
            datum = f"{items.first().datum}"
            year = datum[:3]
            idno = x[2:]
            title_str = f"Aschacher Mautprotokoll {year} (Oberösterreichisches Landesarchiv, Depot Harrach, Handschrift {idno})"
            context = {
                "title": title_str,
                "items": items.count(),
                "from": f"{items.first().datum}",
                "to": f"{items.last().datum}",
                "idno": idno,
                "teis": []
            }
            print(f"gathering data for {title_str}")
            for item in tqdm(items[100:120], total=items.count()):
                context["teis"].append(item.as_tei(full=False).decode('utf-8'))
            context["item_count"] = len(context["teis"])
            print(f"writing {context['item_count']} items into {file_path}")
            with open(file_path, 'w') as f:
                f.write(template.render(context))
