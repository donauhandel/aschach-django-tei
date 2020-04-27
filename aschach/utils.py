norm_patterns = {
    "GND": {
        "regex": '^https?://(?:[^.]*[.])?d-nb.info/gnd/([0-9A-Za-u\-]+)',
        "replace": 'https://d-nb.info/gnd/{}'
    },
    "GeoNames": {
        "regex": '^https?://(?:[^.]*[.])?geonames[.]org/([0-9]+)',
        "replace": 'https://www.geonames.org/{}/'
    }
}


def get_dec(degr):
    try:
        dec = int(degr[0]) + (int(degr[1])/60 + int(degr[2])/3600)
    except Exception as e:
        return None
    return round(dec, 4)
