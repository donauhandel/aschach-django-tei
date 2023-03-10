import lxml.etree as ET

from django.conf import settings
from django.template.loader import get_template

from tei.partials import TEI_NSMAP, TEI_STUMP
from tei.persons import TeiPerson
from tei.places import TeiPlace

ABS = settings.ARCHE_BASE_URL


class MakeTeiDoc():
    def __init__(self, res):
        self.nsmap = TEI_NSMAP
        self.stump = TEI_STUMP
        self.res = res
        self.phaidra = settings.PHAIDRA_BASE
        self.title = f"{self.res.date_german()}"
        self.tree = self.populate_header()

    def get_node_from_template(self, template_path):
        template = get_template(template_path)
        context = {'object': self.res}
        temp_str = f"{template.render(context=context)}"
        node = ET.fromstring(temp_str)
        return node

    def populate_header(self):
        doc = ET.fromstring(self.stump)

        root_el = doc
        root_el.attrib["{http://www.w3.org/XML/1998/namespace}base"] = f"{ABS}/data/"
        root_el.attrib[
            "{http://www.w3.org/XML/1998/namespace}id"
        ] = f"angabe__{self.res.get_formatted_nr()}.xml"
        prev_obj = self.res.get_prev_obj()
        if prev_obj:
            root_el.attrib["prev"] = f"{ABS}/data/angabe__{prev_obj.get_formatted_nr()}.xml"
        next_obj = self.res.get_next_obj()
        if next_obj:
            root_el.attrib["next"] = f"{ABS}/data/angabe__{next_obj.get_formatted_nr()}.xml"

        title_el = doc.xpath('.//tei:title[@type="main"]', namespaces=self.nsmap)[0]
        title_el.text = f"{self.res.date_german()}"

        idno_el = doc.xpath('.//tei:msIdentifier/tei:idno', namespaces=self.nsmap)[0]
        idno_el.text = self.res.get_idno

        tei_facs = doc.xpath('.//tei:facsimile', namespaces=self.nsmap)[0]
        for x in self.res.scan.all():
            graphic_el = ET.Element("{http://www.tei-c.org/ns/1.0}graphic")
            if x.phaidra_id:
                graphic_el.attrib['url'] = self.phaidra.format(x.phaidra_id)
            else:
                graphic_el.attrib['url'] = f"{x.ordner}/{x.datei_name}"
            tei_facs.append(graphic_el)

        msitem_el = doc.xpath('.//tei:msItem', namespaces=self.nsmap)[0]
        locus_el = ET.Element("{http://www.tei-c.org/ns/1.0}locus")
        locusp_el = ET.Element("{http://www.tei-c.org/ns/1.0}p")
        locusp_el.text = self.res.bildnummern.strip()
        if '-' in self.res.bildnummern:
            start, end = self.res.bildnummern.split('-')
            locus_el.attrib['from'] = f"{start.strip()}"
            locus_el.attrib['to'] = f"{end.strip()}"
        else:
            locus_el.attrib['from'] = f"{self.res.bildnummern.strip()}"
            locus_el.attrib['to'] = f"{self.res.bildnummern.strip()}"
        msitem_el.append(locus_el)
        locus_el.addnext(locusp_el)

        origin_el = doc.xpath('.//tei:origin', namespaces=self.nsmap)[0]
        origin_child = ET.Element("{http://www.tei-c.org/ns/1.0}date")
        origin_child.attrib['when-iso'] = f"{self.res.datum}"
        origin_child.text = f"{self.res.date_german()}"
        origin_el.append(origin_child)

        back_el = doc.xpath('.//tei:back', namespaces=self.nsmap)[0]
        listperson_el = ET.Element("{http://www.tei-c.org/ns/1.0}listPerson")
        listplace_el = ET.Element("{http://www.tei-c.org/ns/1.0}listPlace")
        back_el.append(listperson_el)
        back_el.append(listplace_el)

        for x in self.res.get_persons:
            p_el = TeiPerson(x).get_el()
            listperson_el.append(p_el)

        for x in self.res.get_places:
            p_el = TeiPlace(x).get_el()
            listplace_el.append(p_el)

        xeno = doc.xpath('.//tei:teiHeader', namespaces=self.nsmap)[0]
        for x in self.res.get_waren_einheiten['waren']:
            xeno.append(x.as_skos())
        for x in self.res.get_waren_einheiten['einheiten']:
            xeno.append(x.as_skos())

        return doc

    def pop_body(self):
        doc = self.tree
        body_el = doc.xpath('.//tei:body', namespaces=self.nsmap)[0]
        div_el = ET.Element("{http://www.tei-c.org/ns/1.0}div")
        div_el.attrib['type'] = "main"
        div_head_el = ET.Element("{http://www.tei-c.org/ns/1.0}head")
        div_head_el.text = self.title
        div_el.append(div_head_el)
        div_el.append(self.get_node_from_template('tei/fahrzeuge_tei.xml'))
        div_el.append(self.get_node_from_template('tei/angabe_tei.xml'))
        body_el.append(div_el)
        return doc

    def export_full_doc(self):
        return self.pop_body()

    def export_full_doc_str(self, file="temp.xml"):
        with open(file, 'wb') as f:
            f.write(ET.tostring(self.pop_body(), pretty_print=True, encoding='UTF-8'))
        return file
