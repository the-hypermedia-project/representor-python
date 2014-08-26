import unittest

from mock import Mock

from hypermedia_resource import HypermediaResource
from hypermedia_resource.dom import Collection

class TestCollection(unittest.TestCase):

    def setUp(self):
        self.item = Mock(rel='self', href="/customers/1")
        self.collection = Collection(self.item)

    def test_append(self):
        self.assertEqual(len(self.collection.all()), 0)
        self.collection.append(self.item)
        self.assertEqual(len(self.collection.all()), 1)

    def test_add(self):
        self.assertEqual(len(self.collection.all()), 0)
        self.collection.add()
        self.assertEqual(len(self.collection.all()), 1)

class TestHypermediaResource(unittest.TestCase):

    def setUp(self):
        self.resource = HypermediaResource()
        self.attribute = self.resource.attributes.add('name', 'John')
        self.transition = self.resource.transitions.add('self', '/customers/1')
        self.link = self.resource.links.add('customers', '/customers')

    def test_attributes(self):
        name_attr = self.resource.attributes.get('name')
        self.assertEqual(name_attr.value, 'John')

    def test_transitions(self):
        transition = self.resource.transitions.get('self')
        self.assertEqual(transition.href, '/customers/1')

    def test_links(self):
        link = self.resource.links.get('customers')
        self.assertEqual(link.href, '/customers')

if __name__ == '__main__':
    unittest.main()
