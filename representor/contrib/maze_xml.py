import xml.etree.ElementTree as ET
from representor.base import Representor

class MazeXMLAdapter:

    media_type = "application/vnd.amundsen.maze+xml"

    @classmethod
    def parse(self, raw_xml):
        resource = Representor()
        root = ET.fromstring(raw_xml)
        for link in root[0].findall("link"):
            resource.links.add(link.get("rel"), link.get("href"))
        return resource

    @classmethod
    def build(self, resource):
        root = ET.Element('maze')
        root.set('version', '1.0')
        type_of = ET.SubElement(root, resource.meta.attributes.get("type").value)
        for link in resource.links.all():
            new_link = ET.SubElement(type_of, "link")
            new_link.set("rel", link.rel)
            new_link.set("href", link.href)
        return ET.tostring(root, encoding="utf8", method="xml")
