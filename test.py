import unittest

from mock import Mock

from hypermedia_resource import HypermediaResource
from hypermedia_resource.dom import Collection, Item, ItemCollection

class TestItem(unittest.TestCase):

    def setUp(self):
        self.item = Item()

    def test_set(self):
        self.item.set('foo', 'bar')
        self.assertEqual(self.item.foo, 'bar')

class TestCollection(unittest.TestCase):

    def setUp(self):
        self.collection = Collection()

    def test_init(self):
        self.assertEqual(len(self.collection), 0)

    def test_append(self):
        value = self.collection.append("Foobar")
        self.assertEqual(len(self.collection), 1)

    def test_add(self):
        self.collection.add("Hello", "World")
        self.assertEqual(len(self.collection), 2)

    def test_len(self):
        self.collection.add("Foobar")
        self.assertEqual(len(self.collection), 1)

    def test_all(self):
        self.collection.add("Hello", "World")
        self.assertEqual(self.collection.all(), ["Hello", "World"])

    def test_set_items(self):
        items = ["Hello", "World"]
        self.collection.set_items(items)
        self.assertEqual(self.collection.all(), items)

    def test_iter(self):
        items = ["Hello", "World"]
        self.collection.set_items(items)
        self.assertEqual([item for item in self.collection], items)

class TestItemCollection(unittest.TestCase):

    def setUp(self):
        self.item = Item
        self.collection = ItemCollection()

    def test_init(self):
        self.assertEqual(len(self.collection.all()), 0)

    def test_set_item_type(self):
        self.collection.set_item_type(self.item)
        self.assertEqual(self.collection.item, self.item)

    def test_add(self):
        self.collection.set_item_type(self.item)
        self.collection.add()
        self.assertEqual(len(self.collection.all()), 1)

    def test_filter_by(self):
        item1 = self.item()
        item1.set('var1', 'value1')
        item2 = self.item()
        item2.set('var1', 'value1')
        item3 = self.item()
        item3.set('var1', 'value2')
        self.collection.set_items([item1, item2, item3])
        self.assertEqual(len(self.collection.filter_by('var1', 'value1')), 2)

class TestHypermediaResource(unittest.TestCase):

    def setUp(self):
        self.resource = HypermediaResource()

    def test_attributes(self):
        self.attribute = self.resource.attributes.add('name', 'John')
        name_attr = self.resource.attributes.get('name')
        self.assertEqual(name_attr.value, 'John')

    def test_transitions(self):
        self.resource.transitions.add('self', '/customers/1')
        transition = self.resource.transitions.get('self')
        self.assertEqual(transition.href, '/customers/1')

    def test_links(self):
        self.resource.links.add('customers', '/customers')
        link = self.resource.links.get('customers')
        self.assertEqual(link.href, '/customers')

    def test_queries(self):
        self.resource.queries.add('search', '/customers')
        query = self.resource.queries.get('search')
        self.assertEqual(query.href, '/customers')

    def test_actions(self):
        self.resource.actions.add('append', '/customers', 'POST')
        action = self.resource.actions.get('append')
        self.assertEqual(action.href, '/customers')

    def test_meta_attributes(self):
        self.attribute = self.resource.meta.attributes.add('name', 'John')
        name_attr = self.resource.meta.attributes.get('name')
        self.assertEqual(name_attr.value, 'John')

    def test_meta_links(self):
        self.resource.meta.links.add('profile', 'http://example.com/customers')
        meta_link = self.resource.meta.links.get('profile')
        self.assertEqual(meta_link.href, 'http://example.com/customers')

if __name__ == '__main__':
    unittest.main()
