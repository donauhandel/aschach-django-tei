import re
from tqdm import tqdm
from aschach.utils import get_krems_places, get_dec
from aschach.models import Ort
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "enriches Places with Krems-DB data"

    # A command must define handle()
    def handle(self, *args, **options):
        df = get_krems_places()
        no_match = []
        match = []
        for i, row in tqdm(df.iterrows(), total=len(df)):
            try:
                ort = Ort.objects.get(legacy_pk=row["aschachId"])
            except:
                no_match.append([row["aschachId"], row["ortsname"]])
            match.append([row["aschachId"], row["ortsname"]])
            lat_degree = row["latitude"]
            long_degree = row["longitude"]
            if isinstance(lat_degree, str):
                lat_degree = [int(x) for x in re.findall(r"\d+", lat_degree)]
                lat = get_dec(lat_degree)
                long_degree = [int(x) for x in re.findall(r"\d+", long_degree)]
                lat = get_dec(lat_degree)
                lng = get_dec(long_degree)
                ort.lat = lat
                ort.lng = lng
                ort.save()
        print(f"found {len(match)} matching Places")
