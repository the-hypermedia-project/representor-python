import xml.etree.ElementTree as ET
import unittest
import json

from hypermedia_resource import HypermediaResource
from hypermedia_resource.contrib.maze_xml import MazeXMLAdapter

cell_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<maze version="1.0">
    <cell>
        <link href="http://amundsen.com/examples/mazes/2d/five-by-five/0:north" rel="current" debug="0:1,1,1,0" total="25" side="5" />
        <link href="http://amundsen.com/examples/mazes/2d/five-by-five/5:east" rel="east" />
    </cell>
</maze>"""

class TestClass(unittest.TestCase):

    def test_media_type(self):
        self.assertEqual(MazeXMLAdapter.media_type,
                         "application/vnd.amundsen.maze+xml")

class TestParse(unittest.TestCase):

    def setUp(self):
        HypermediaResource.adapters.add(MazeXMLAdapter)
        self.resource = HypermediaResource.adapters.translate_from("application/vnd.amundsen.maze+xml",
                                                                    cell_xml)

    def tearDown(self):
        HypermediaResource.reset_adapters()

    def test_parse_links(self):
        links = self.resource.links.all()
        self.assertEqual(len(links), 2)
        self.assertEqual(len(self.resource.links.filter_by_rel("current")), 1)

    def test_type(self):
        pass

class TestBuild(unittest.TestCase):

    def setUp(self):
        HypermediaResource.adapters.add(MazeXMLAdapter)
        self.resource = HypermediaResource()
        self.resource.meta.attributes.add("type", "cell")
        self.resource.links.add("current", "http://example.com/cell/2")
        self.resource.links.add("east", "http://example.com/cell/3")
        self.raw_xml = self.resource.translate_to("application/vnd.amundsen.maze+xml")

    def tearDown(self):
        HypermediaResource.reset_adapters()

    def test_build(self):
        root = ET.fromstring(self.raw_xml)
        self.assertEqual(root[0].tag, "cell")
        self.assertEqual(len(root[0].findall("link")), 2)


