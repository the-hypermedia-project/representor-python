import unittest

from hypermedia_resource.base import Collection

class StubItem:
    pass

class TestCollection(unittest.TestCase):

    def setUp(self):
        self.collection = Collection()

    def test_append(self):
        self.assertEqual(len(self.collection._items), 0)
        self.collection.append('test')
        self.assertEqual(len(self.collection._items), 1)

if __name__ == '__main__':
    unittest.main()
