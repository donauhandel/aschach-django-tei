import datetime
import lxml.etree as ET

from tei.partials import TEI_NSMAP, TEI_STUMP, custom_escape


class TeiPlace():
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
        if self.res.region:
            region_el = ET.Element("{http://www.tei-c.org/ns/1.0}region")
            region_el.text = self.res.region.name
            name.append(region_el)
            item.append(name)
        return item
