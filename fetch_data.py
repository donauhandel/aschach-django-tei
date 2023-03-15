import re
import os
import shutil
import requests

to_ingest = "to_ingest"
shutil.rmtree(to_ingest, ignore_errors=True)

os.makedirs(to_ingest, exist_ok=True)

URL = "https://dh-aschach.acdh-dev.oeaw.ac.at/media/tei_out/"

r = requests.get(URL)

regex = r""">DepHarr_H\d*\.xml<"""

matches = re.findall(pattern=regex, string=r.text)
for x in matches:
    f_name = x[1:-1]
    f_path = os.path.join(to_ingest, f_name)
    f_url = f"{URL}{f_name}"
    r = requests.get(f_url, allow_redirects=True)
    print(f"downloading {f_name} from {f_url}")
    with open(f_path, 'wb') as f:
        f.write(r.content)