import sys
import unittest
import json
import logging

from hypermedia_resource import HypermediaResource
from hypermedia_resource.adapters.hale_json import HaleJSONAdapter

hale_example = """{
    "_meta": {
        "any": {
            "json": "object"
        }
    },
    "attribute": "value",
    "_links": {
        "self": {
            "href": "..."
        },
        "search": {
            "href": ".../{?send_info}",
            "templated": true,
            "method": "GET",
            "data": {
                "send_info": {
                    "options": [
                        "yes",
                        "no",
                        "maybe"
                    ],
                    "in": true
                }
            }
        },
        "agent": {
            "href": "/agent/1",
            "method": "GET",
            "render": "embed"
        },
        "customer": [
            {
                "href": "/customer/1",
                "method": "GET"
            }
        ],
        "edit-customer": {
            "href": ".../1",
            "method": "PUT",
            "request_encoding": "application/json",
            "data": {
                "name": {
                    "type": "string",
                    "required": true
                },
                "send_info": {
                    "options": [
                        "yes",
                        "no",
                        "maybe"
                    ],
                    "in": true
                },
                "user_id": {
                    "scope": "href",
                    "required": true
                }
            }
        }
    },
    "_embedded": {
        "customer": [
            {
                "_links": {
                    "self": {
                        "href": "/customer/1",
                        "method": "GET"
                    },
                    "edit": {
                        "href": ".../{?user_id}",
                        "method": "PUT",
                        "request_encoding": "application/json",
                        "render": "resource",
                        "data": {
                            "name": {
                                "type": "string",
                                "required": true
                            },
                            "send_info": {
                                "options": [
                                    "yes",
                                    "no",
                                    "maybe"
                                ],
                                "in": true
                            },
                            "user_id": {
                                "scope": "href",
                                "required": true
                            }
                        }
                    }
                },
                "name": "Tom",
                "send_info": "yes"
            }
        ]
    }
}"""

class TestParse(unittest.TestCase):

    def setUp(self):
        HypermediaResource.adapters.add(HaleJSONAdapter)
        self.resource = HypermediaResource.adapters.translate_from("application/vnd.hale+json",
                                                                   hale_example)

    def tearDown(self):
        HypermediaResource.reset_adapters()

    def test_attributes(self):
        attr = self.resource.attributes.get("attribute")
        self.assertEqual(attr.value, "value")

    def test_links(self):
        self_links = self.resource.links.filter_by_rel("self")
        self.assertEqual(len(self_links), 1)
        self_link = self.resource.links.get("self")
        self.assertEqual(self_link.href, "...")
        self.assertEqual(len(self.resource.links.all()), 3)

    def test_actions(self):
        edit_customer = self.resource.actions.get("edit-customer")
        self.assertEqual(edit_customer.method, "PUT")
        request_type = edit_customer.response_types.filter_by("media_type", "application/json")
        self.assertEqual(len(request_type), 1)
        self.assertEqual(len(edit_customer.attributes.all()), 3)
        send_info = edit_customer.attributes.filter_by("name", "send_info")[0]
        self.assertEqual(len(send_info.options.all()), 3)

    def test_embedded(self):
        logging.basicConfig( stream=sys.stderr )
        log = logging.getLogger("TestParse.test_embedded")
        customer = self.resource.embedded_resources.get("customer")
        log.debug(customer.attributes.all())
        self.assertEqual(customer.attributes.get("name").value, "Tom")

