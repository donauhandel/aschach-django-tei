import lxml.etree as ET

from tei.partials import TEI_NSMAP, TEI_STUMP


class TeiPerson:
    def __init__(self, res):
        self.nsmap = TEI_NSMAP
        self.stump = TEI_STUMP
        self.res = res

    def get_el(self):
        item = ET.Element("{http://www.tei-c.org/ns/1.0}person")
        item.attrib[
            "{http://www.w3.org/XML/1998/namespace}id"
        ] = f"person__{self.res.id}"
        name = ET.Element("{http://www.tei-c.org/ns/1.0}persName")
        item.append(name)

        f_name = ET.Element("{http://www.tei-c.org/ns/1.0}forename")
        if self.res.vorname:
            f_name.text = f"{self.res.vorname.name}"
        else:
            f_name.text = "N."
        name.append(f_name)

        f_name = ET.Element("{http://www.tei-c.org/ns/1.0}surname")
        if self.res.nachname:
            f_name.text = f"{self.res.nachname.name}"
        else:
            f_name.text = "N."
        name.append(f_name)
        for x in self.res.normdata_url.all():
            idno_el = ET.Element("{http://www.tei-c.org/ns/1.0}idno")
            idno_el.attrib["subtype"] = x.domain.replace(" ", "").strip().lower()
            idno_el.attrib["type"] = "URL"
            idno_el.text = x.uri
            item.append(idno_el)

        return item
