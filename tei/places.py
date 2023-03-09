import lxml.etree as ET

from tei.partials import TEI_NSMAP, TEI_STUMP


class TeiPlace:
    def __init__(self, res):
        self.nsmap = TEI_NSMAP
        self.stump = TEI_STUMP
        self.res = res

    def get_el(self):
        item = ET.Element("{http://www.tei-c.org/ns/1.0}place")
        item.attrib[
            "{http://www.w3.org/XML/1998/namespace}id"
        ] = f"place__{self.res.id}"
        name = ET.Element("{http://www.tei-c.org/ns/1.0}placeName")
        name.text = self.res.name
        item.append(name)
        if self.res.region:
            region_el = ET.Element("{http://www.tei-c.org/ns/1.0}region")
            region_el.text = self.res.region.name
            item.append(region_el)
        if self.res.lat:
            loc_el = ET.Element("{http://www.tei-c.org/ns/1.0}location")
            geo_el = ET.Element("{http://www.tei-c.org/ns/1.0}geo")
            item.append(loc_el)
            loc_el.append(geo_el)
            geo_el.attrib["decls"] = "LatLng"
            geo_el.text = f"{self.res.lat} {self.res.lng}"
        for x in self.res.normdata_url.all():
            idno_el = ET.Element("{http://www.tei-c.org/ns/1.0}idno")
            idno_el.attrib["subtype"] = x.domain.replace(" ", "").strip().lower()
            idno_el.attrib["type"] = "URL"
            idno_el.text = x.uri
            item.append(idno_el)
        return item
