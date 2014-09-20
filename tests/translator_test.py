import unittest
from mock import Mock
from hypermedia_resource.translator import Translator

def adapter():
    adapter = Mock()
    adapter.media_type = "application/hal+json"
    adapter.parse.return_value = "parsed"
    adapter.build.return_value = "built"
    return adapter

class TestInit(unittest.TestCase):

    def test_init_with_adapter(self):
        self.adapter = adapter()
        translator = Translator(adapter)
        self.assertEqual(len(translator.all()), 1)

class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.adapter = adapter()
        self.translator = Translator(self.adapter)

    def test_get(self):
        adapter = self.translator.get("application/hal+json")
        self.assertEqual(self.adapter, adapter)

    def test_register(self):
        self.assertEqual(len(self.translator.all()), 1)

    def test_translate_from(self):
        resource = self.translator.translate_from("application/hal+json",
                                                  { "foo": "bar" })
        self.assertEqual(resource, "parsed")
        self.adapter.parse.assert_called_with({ "foo": "bar" })

    def test_translate_to(self):
        resource = Mock()
        rep = self.translator.translate_to("application/hal+json", resource)
        self.assertEqual(rep, "built")
        self.adapter.build.assert_called_with(resource)

    def test_get_media_types(self):
        media_types = self.translator.get_media_types()
        self.assertEqual(media_types, ["application/hal+json"])
