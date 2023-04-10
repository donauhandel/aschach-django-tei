import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from tqdm import tqdm

from aschach.models import Angabe


class Command(BaseCommand):
    # Show this when the user types help
    help = "updates Angaben"

    # A command must define handle()
    def handle(self, *args, **options):
        DATA_REPO_URL = settings.DATA_REPO_URL
        df = pd.read_csv(f"{DATA_REPO_URL}/angaben.csv").dropna()
        for i, row in tqdm(df.iterrows(), total=len(df)):
            item = Angabe.objects.get(legacy_pk=row["angabenId"])
            item.datum_original = row["datum"]
            item.datum = row["datum"].replace("/", "-")
            item.quelle = row["quelle"]
            item.save()
        print("done")
