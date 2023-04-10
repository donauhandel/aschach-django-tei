import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm

from aschach.models import Angabe


class Command(BaseCommand):
    # Show this when the user types help
    help = "updates Angaben"

    # A command must define handle()
    def handle(self, *args, **options):
        no_match = []
        DATA_REPO_URL = settings.DATA_REPO_URL
        df = pd.read_csv(f"{DATA_REPO_URL}/angaben.csv").dropna()
        for i, row in tqdm(df.iterrows(), total=len(df)):
            try:
                item, _ = Angabe.objects.get_or_create(legacy_pk=row["angabenId"])
            except ObjectDoesNotExist:
                no_match.append(row["angabenId"])
                continue
            item.datum_original = row["datum"]
            item.datum = row["datum"].replace("/", "-")
            item.quelle = row["quelle"]
            item.save()
        print("done")
        print("no match for following ids")
        for x in no_match:
            print(x)
