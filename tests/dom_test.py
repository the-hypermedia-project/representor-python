import unittest
from representor.dom import Collection, Item, ItemCollection

class TestItem(unittest.TestCase):

    def setUp(self):
        self.item = Item()

    def test_set(self):
        self.item.set("foo", "bar")
        self.assertEqual(self.item.foo, "bar")

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
        item1.set("var1", "value1")
        item2 = self.item()
        item2.set("var1", "value1")
        item3 = self.item()
        item3.set("var1", "value2")
        self.collection.set_items([item1, item2, item3])
        self.assertEqual(len(self.collection.filter_by("var1", "value1")), 2)
