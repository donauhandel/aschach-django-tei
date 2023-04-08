import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from tqdm import tqdm

from aschach.models import Scan


class Command(BaseCommand):
    # Show this when the user types help
    help = "adds missing phaidra ids"

    # A command must define handle()
    def handle(self, *args, **options):
        no_scan = Scan.objects.filter(phaidra_id="")
        print(f"{no_scan.count()} Scans without Phaidra ID")
        DATA_REPO_URL = settings.DATA_REPO_URL
        df = pd.read_csv(f"{DATA_REPO_URL}/scans.csv").dropna()
        for i, row in tqdm(df.iterrows(), total=len(df)):
            item = Scan.objects.get(legacy_pk=row["scanId"])
            item.phaidra_id = row["phaidra"]
            item.datei_name = row["datei"]
            item.ordner = row["ordner"]
            item.save()
        no_scan = Scan.objects.filter(phaidra_id="")
        print(f"{no_scan.count()} Scans without Phaidra ID")
