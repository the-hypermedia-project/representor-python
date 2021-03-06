import unittest
from mock import Mock, patch
from representor import Representor
from representor.wrappers import HypermediaResponse, ResponseBuilder
from representor.wrappers import APIResource, FlaskAPIResource

def adapter():
    adapter = Mock()
    adapter.media_type = "application/hal+json"
    adapter.parse.return_value = "parsed"
    adapter.build.return_value = "built"
    return adapter

def request(method='GET', form={}):
    request = Mock()
    request.method = method
    request.form = form
    request.headers = Mock()
    request.headers.get = Mock()
    request.headers.get.return_value = "application/hal+json"
    return request

class TestHypermediaResponse(unittest.TestCase):

    def test(self):
        resource = Representor()
        resource.adapters.add(adapter())
        response = HypermediaResponse("application/hal+json", resource)
        self.assertEqual(response.media_type, "application/hal+json")
        self.assertEqual(response.body, "built")

class TestResponseBuilder(unittest.TestCase):

    def test(self):
        resource = Representor()
        resource.adapters.add(adapter())
        accept = "application/hal+json"
        response_builder = ResponseBuilder("application/hal+json")
        response = response_builder.build(resource, accept)
        self.assertEqual(response.media_type, "application/hal+json")
        self.assertEqual(response.body, "built")

class TestAPIResource(unittest.TestCase):

    def setUp(self):
        Representor.adapters.add(adapter())
        self.resource = APIResource()

    def test_available_actions(self):
        self.resource.read = Mock()
        actions = self.resource.available_actions()
        self.assertTrue('read' in actions)
        self.assertFalse('missing' in actions)

    def test_available_methods(self):
        self.resource.read = Mock()
        methods = self.resource.available_methods()
        self.assertTrue('GET' in methods)
        self.assertFalse('POST' in methods)

    def test_response(self):
        resource = Representor()
        self.resource.read = Mock()
        self.resource.read.return_value = resource
        accepts = "application/hal+json"
        response = self.resource.build_response(resource, accepts)
        self.assertEqual(response.body, "built")

class TestFlaskAPIResource(unittest.TestCase):

    def setUp(self):
        self.resource = FlaskAPIResource()

    def test_get_method(self):
        method = self.resource.get_method(request("GET"))
        self.assertEqual(method, "GET")

    def test_get_method_override(self):
        method = self.resource.get_method(request("POST", { "_method": "PUT"}))
        self.assertEqual(method, "PUT")

    def test_response_for(self):
        resource = Representor()

        # Mock HypermediaResponse so we don't have to translate a resource
        hypermedia_response = Mock()
        hypermedia_response.media_type = "application/hal+json"
        hypermedia_response.body = "{ \"foo\": \"bar\" }"

        # Mock build response to return the mocked hypermedia_response
        self.resource.build_response = Mock()
        self.resource.build_response.return_value = hypermedia_response

        # Mock read action on a Flask API resource
        self.resource.read = Mock()
        self.resource.read.return_value = resource

        response = self.resource.response_for(request('GET', {}))
        self.assertEqual(response.mimetype, "application/hal+json")
        self.assertEqual(response.data, "{ \"foo\": \"bar\" }")
