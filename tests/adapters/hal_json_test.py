import unittest
import json

from mock import Mock

from hypermedia_resource import HypermediaResource
from hypermedia_resource.adapters.hal_json import HalJSONAdapter

hal_example = """{
    "_links": {
        "self": { "href": "/orders" },
        "curies": [{ "name": "ea", "href": "http://example.com/docs/rels/{rel}", "templated": true }],
        "next": { "href": "/orders?page=2" },
        "ea:find": {
            "href": "/orders{?id}",
            "templated": true
        },
        "ea:admin": [{
            "href": "/admins/2",
            "title": "Fred"
        }, {
            "href": "/admins/5",
            "title": "Kate"
        }]
    },
    "currentlyProcessing": 14,
    "shippedToday": 20,
    "_embedded": {
        "ea:order": [{
            "_links": {
                "self": { "href": "/orders/123" },
                "ea:basket": { "href": "/baskets/98712" },
                "ea:customer": { "href": "/customers/7809" }
            },
            "total": 30.00,
            "currency": "USD",
            "status": "shipped"
        }, {
            "_links": {
                "self": { "href": "/orders/124" },
                "ea:basket": { "href": "/baskets/97213" },
                "ea:customer": { "href": "/customers/12369" }
            },
            "total": 20.00,
            "currency": "USD",
            "status": "processing"
        }]
    }
}"""

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

    def test_links(self):
        self.resource.links.add('self', '/customers/1')
        self.resource.links.add('order', '/customers/1/orders/4')
        self.resource.links.add('order', '/customers/1/orders/5')
        json_hal_rep = self.resource.translate_to("application/hal+json")
        hal_rep = json.loads(json_hal_rep)
        self.assertTrue("_links" in hal_rep)
        self.assertTrue(type(hal_rep["_links"]["self"]) is dict)
        self.assertTrue(type(hal_rep["_links"]["order"]) is list)
        self.assertEqual(len(hal_rep["_links"].keys()), 2)

    def test_profile(self):
        pass

    def test_hreflang(self):
        pass

    def test_deprecated(self):
        pass

    def test_title(self):
        pass

    def test_embedded(self):
        pass

    def test_templated(self):
        pass

class TestParse(unittest.TestCase):

    def setUp(self):
        HypermediaResource.register(HalJSONAdapter)
        self.resource = HypermediaResource.translate_from("application/hal+json",
                                                          hal_example)

    def test_attributes(self):
        attr = self.resource.attributes.get("shippedToday")
        self.assertEqual(attr.value, 20)

    def test_links(self):
        next_links = self.resource.links.filter_by_rel("next")
        self.assertEqual(len(next_links), 1)
        admin_links = self.resource.links.filter_by_rel("ea:admin")
        self.assertEqual(len(admin_links), 2)
        self_link = self.resource.links.get("self")
        self.assertEqual(self_link.href, "/orders")
        self.assertEqual(len(self.resource.links.all()), 4)

    def test_profile(self):
        pass

    def test_hreflang(self):
        pass

    def test_deprecated(self):
        pass

    def test_title(self):
        pass

    def test_embedded(self):
        pass

    def test_templated(self):
        pass




