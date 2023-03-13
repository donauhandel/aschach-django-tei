from tqdm import tqdm
from aschach.models import Angabe
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "denormalizes Angabe-Ware"

    # A command must define handle()
    def handle(self, *args, **options):
        items = Angabe.objects.all()
        for x in tqdm(items, total=items.count()):
            waren = x.get_waren()
            x.related_goods.set(waren)
        print("done")
