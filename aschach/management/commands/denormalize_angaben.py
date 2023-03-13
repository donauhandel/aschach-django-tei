from tqdm import tqdm
from aschach.models import Angabe
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "denormalizes Angabe with Waren, Personen und Orten"

    # A command must define handle()
    def handle(self, *args, **options):
        items = Angabe.objects.all()
        for x in tqdm(items, total=items.count()):
            waren = x.get_waren()
            x.related_good.set(waren)
            persons = x.get_persons
            x.related_person.set(persons)
            places = x.get_places
            x.related_place.set(places)
        print("done")
