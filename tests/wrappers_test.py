import unittest
from mock import Mock
from hypermedia_resource import HypermediaResource
from hypermedia_resource.wrappers import HypermediaResponse, ResponseBuilder

def adapter():
    adapter = Mock()
    adapter.media_type = "application/hal+json"
    adapter.parse.return_value = "parsed"
    adapter.build.return_value = "built"
    return adapter

class TestHypermediaResponse(unittest.TestCase):

    def test(self):
        resource = HypermediaResource()
        resource.adapters.add(adapter())
        response = HypermediaResponse("application/hal+json", resource)
        self.assertEqual(response.media_type, "application/hal+json")
        self.assertEqual(response.body, "built")

class TestResponseBuilder(unittest.TestCase):

    def test(self):
        resource = HypermediaResource()
        resource.adapters.add(adapter())
        accept = "application/hal+json"
        response_builder = ResponseBuilder("application/hal+json")
        response = response_builder.build(resource, accept)
        self.assertEqual(response.media_type, "application/hal+json")
        self.assertEqual(response.body, "built")
