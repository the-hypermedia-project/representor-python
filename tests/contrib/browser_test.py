import unittest

from hypermedia_resource import HypermediaResource
from hypermedia_resource.contrib.browser import BrowserAdapter

class BrowserTest(unittest.TestCase):

    def setUp(self):
        HypermediaResource.adapters.add(BrowserAdapter)
        self.resource = HypermediaResource()

    def tearDown(self):
        HypermediaResource.reset_adapters()

    def test_links(self):
        self.resource.links.add("self", "/example")
        html = self.resource.translate_to("text/html")
        self.assertTrue('href="/example"' in html)

    def test_link_label_set(self):
        self.resource.links.add("self", "/example", label="Test Link!")
        html = self.resource.translate_to("text/html")
        self.assertTrue('>Test Link!</a>' in html)

    def test_link_not_set(self):
        self.resource.links.add("self", "/example", label="Test Link!")
        html = self.resource.translate_to("text/html")
        self.assertTrue('rel="self"' in html)

    def test_page_title_set(self):
        self.resource.meta.attributes.add("title", "Test")
        html = self.resource.translate_to("text/html")
        self.assertTrue('<h1>Test</h1>' in html)
        self.assertTrue('<title>Test</title>' in html)

    def test_page_title_not_set(self):
        html = self.resource.translate_to("text/html")
        self.assertTrue('<h1>Hypermedia Browser</h1>' in html)
        self.assertTrue('<title>Hypermedia Browser</title>' in html)

