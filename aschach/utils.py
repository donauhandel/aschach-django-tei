import requests
import pandas as pd
from io import StringIO

ORTE_CSV_URL = "https://raw.githubusercontent.com/donauhandel/krems-data/main/orig_data/csvs/orte.csv"


def get_krems_places():
    r = requests.get(ORTE_CSV_URL)
    df = pd.read_csv(StringIO(r.text))
    df = df[df["aschachId"].notna()]
    df["aschachId"].astype("int")
    return df


def get_dec(degr):
    try:
        dec = int(degr[0]) + (int(degr[1]) / 60 + int(degr[2]) / 3600)
    except:
        return None
    return round(dec, 4)
