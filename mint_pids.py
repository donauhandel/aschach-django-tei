import requests
import os
import json
from acdh_handle_pyutils.client import HandleClient
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

HD_PW = os.environ.get("HANDLE_PW")
HD_USER = os.environ.get("HANDLE_USER")
client = HandleClient(HD_USER, HD_PW)

ARCHE = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")

URL = "https://dh-aschach.acdh-dev.oeaw.ac.at/media/tei_out/"

r = requests.get(f"{URL}/arche.ttl")
body = r.text
with open("arche.ttl", "w") as f:
    f.write(body)

g = Graph()
g.parse("arche.ttl")
data = {}
for s in g.subjects(RDF.type, ARCHE["Resource"]):
    pid = client.register_handle(f"{s}")
    data[f"{s}"] = pid

with open("pids.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)
