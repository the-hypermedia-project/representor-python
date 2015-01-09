import unittest

from representor import HypermediaResource
from representor.contrib.browser import BrowserAdapter

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

    def test_attributes(self):
        self.resource.attributes.add("foo", "bar")
        self.resource.attributes.add("hello", "world", label="Hello Attr")
        html = self.resource.translate_to("text/html")
        self.assertTrue('<dt>foo</dt>' in html)
        self.assertTrue('<dd>bar</dd>' in html)
        self.assertTrue('<dt>Hello Attr</dt>' in html)

    def test_queries(self):
        query = self.resource.queries.add("search", "/search")
        query.params.add("search_key")
        query.params.add("another", "value-given")
        html = self.resource.translate_to("text/html")
        self.assertTrue('<form method="GET" action="/search"' in html)
        self.assertTrue('name="search_key"' in html)
        self.assertTrue('name="another" value="value-given"' in html)

    def test_options(self):
        query = self.resource.queries.add("search", "/search")
        param = query.params.add("search_key", "red")
        param.options.add("Bar", "bar")
        param.options.add("Red", "red")
        html = self.resource.translate_to("text/html")
        self.assertTrue('<select name="search_key"' in html)
        self.assertTrue('value="bar">Bar' in html)
        self.assertTrue('selected="selected" value="red">Red' in html)

    def test_actions_override(self):
        action = self.resource.actions.add("create", "/users", "POST", label="Create User")
        attribute = action.attributes.add("username")
        html = self.resource.translate_to("text/html")
        self.assertTrue('name="_method" value="PUT"' in html)

    def test_actions_override(self):
        action = self.resource.actions.add("update", "/users", "PUT", label="Update User")
        attribute = action.attributes.add("username", "johndoe")
        html = self.resource.translate_to("text/html")
        self.assertTrue('name="_method" value="PUT"' in html)

    def test_embedded(self):
        embedded = self.resource.embedded_resources.add("item", "/embed")
        embedded.attributes.add("name", "John Doe")
        embedded.links.add("self", "/example", label="Test Link!")
        html = self.resource.translate_to("text/html")
        self.assertTrue('<dd>John Doe</dd>' in html)
        self.assertTrue('rel="self"' in html)
