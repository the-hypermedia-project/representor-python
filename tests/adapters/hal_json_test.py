import unittest
import json

from mock import Mock

from hypermedia_resource import HypermediaResource
from hypermedia_resource.adapters.hal_json import HalJSONAdapter

class TestClass(unittest.TestCase):

    def test_media_type(self):
        self.assertEqual(HalJSONAdapter.media_type,
                         "application/hal+json")

class TestBuild(unittest.TestCase):

    def setUp(self):
        HypermediaResource.register(HalJSONAdapter)
        self.resource = HypermediaResource()

    def test_properties(self):
        self.resource.attributes.add("foo", "bar")
        json_hal_rep = self.resource.translate_to("application/hal+json")
        hal_rep = json.loads(json_hal_rep)
        self.assertEqual(hal_rep["foo"], "bar")


