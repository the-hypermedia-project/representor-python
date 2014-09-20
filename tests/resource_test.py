import unittest
from mock import Mock
from hypermedia_resource import HypermediaResource

class TestTranslator(unittest.TestCase):

    def setUp(self):
        # Reset class variable
        HypermediaResource._adapters = {}
        self.adapter = Mock()
        self.adapter.media_type = "application/hal+json"
        self.adapter.parse.return_value = "parsed"
        self.adapter.build.return_value = "built"

    def test_register(self):
        HypermediaResource.register(self.adapter)
        self.assertEqual(len(HypermediaResource._adapters.items()), 1)

    def test_translate_from(self):
        HypermediaResource.register(self.adapter)
        resource = HypermediaResource.translate_from("application/hal+json",
                                                     { "foo": "bar" })
        self.assertEqual(resource, "parsed")
        self.adapter.parse.assert_called_with({ "foo": "bar" })

    def test_translate_to(self):
        HypermediaResource.register(self.adapter)
        resource = HypermediaResource()
        rep = resource.translate_to("application/hal+json")
        self.assertEqual(rep, "built")
        self.adapter.build.assert_called_with(resource)

class TestHypermediaResource(unittest.TestCase):

    def setUp(self):
        self.resource = HypermediaResource()

    def test_translate_from(self):
        adapter = Mock()
        adapter.media_type = "application/hal+json"
        adapter.parse

    def test_attributes(self):
        self.attribute = self.resource.attributes.add("name", "John")
        name_attr = self.resource.attributes.get("name")
        self.assertEqual(name_attr.value, "John")

    def test_transitions(self):
        # This creates a link and also adds it to transitions
        link = self.resource.links.add("self", "/customers/1")
        # This adds the same link to transitions, making two total
        self.resource.transitions.add(link)
        transitions_count = len(self.resource.transitions.all())
        self.assertEqual(transitions_count, 2)

    def test_links(self):
        self.resource.links.add("customers", "/customers")
        link = self.resource.links.get("customers")
        self.assertEqual(link.href, "/customers")

    def test_queries(self):
        self.resource.queries.add("search", "/customers")
        query = self.resource.queries.get("search")
        self.assertEqual(query.href, "/customers")

    def test_actions(self):
        self.resource.actions.add("append", "/customers", "POST")
        action = self.resource.actions.get("append")
        self.assertEqual(action.href, "/customers")

    def test_meta_attributes(self):
        self.attribute = self.resource.meta.attributes.add("name", "John")
        name_attr = self.resource.meta.attributes.get("name")
        self.assertEqual(name_attr.value, "John")

    def test_meta_links(self):
        self.resource.meta.links.add("profile", "http://example.com/customers")
        meta_link = self.resource.meta.links.get("profile")
        self.assertEqual(meta_link.href, "http://example.com/customers")

class TestTransitionCollection(unittest.TestCase):

    def setUp(self):
        self.resource = HypermediaResource()

    def test_get_rels(self):
        self.resource.links.add("self", "/customers/1")
        self.resource.links.add("orders", "/customers/1/orders")
        self.resource.links.add("addresses", "/customers/1/addresses")
        rels = self.resource.transitions.get_rels()
        self.assertEqual(rels, ["self", "orders", "addresses"])
