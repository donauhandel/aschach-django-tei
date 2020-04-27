import lxml.etree as ET
from django.template.loader import get_template


def skosify_ware_from_template(res, template_path):
    template = get_template(template_path)
    context = {'object': res}
    temp_str = f"{template.render(context=context)}"
    node = ET.fromstring(temp_str)
    return node
