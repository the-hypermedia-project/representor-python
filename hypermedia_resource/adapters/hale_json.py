import json
from hypermedia_resource.base import HypermediaResource

RESERVED_ATTRIBUTES = ["_links", "_embedded"]

def parse_attributes(hal_rep, resource):
    attrs = [[key, value] for key, value in hal_rep.items()
                if key not in RESERVED_ATTRIBUTES]
    for attr in attrs:
        resource.attributes.add(attr[0], attr[1])

def parse_link(rel, link, resource):
    if "templated" in link and link["templated"]:
        return
    if (link.has_key("method") and link["method"] != "GET"):
        resource = resource.actions.add(rel, link["href"], link["method"])
    else:
        resource = resource.links.add(rel=rel, href=link["href"])
    if link.has_key("request_encoding"):
        resource.response_types.add(link["request_encoding"])
    if link.has_key("data"):
        # Right now, it only supports name and values
        for name, value in link["data"].items():
            attr = resource.attributes.add(name)
            if value.has_key("options"):
                for option in value["options"]:
                    attr.options.add(option, option)
    return resource

def parse_links(hal_rep, resource):
    if not "_links" in hal_rep or not hal_rep["_links"]:
        return
    for rel, link in hal_rep["_links"].items():
        if type(link) is dict:
            parse_link(rel, link, resource)
        else:
            for item in link:
                parse_link(rel, item, resource)

def parse_embedded(rel, embedded, resource):
    href = embedded["_links"]["self"]
    item = resource.embedded_resources.add(rel, href)
    parse_attributes(embedded, item)
    parse_links(embedded, item)
    parse_embeddeds(embedded, item)
    return item

def parse_embeddeds(hal_rep, resource):
    if not "_embedded" in hal_rep or not hal_rep["_embedded"]:
        return
    for rel, link in hal_rep["_embedded"].items():
        if type(link) is dict:
            parse_embedded(rel, link, resource)
        else:
            for item in link:
                parse_embedded(rel, item, resource)

class HaleJSONAdapter(object):

    media_type = "application/vnd.hale+json"

    @classmethod
    def parse(self, raw_json):
        hal_rep = json.loads(raw_json)
        resource = HypermediaResource()
        parse_attributes(hal_rep, resource)
        parse_links(hal_rep, resource)
        parse_embeddeds(hal_rep, resource)
        return resource
