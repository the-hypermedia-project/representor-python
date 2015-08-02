import json
from representor.base import Representor

RESERVED_ATTRIBUTES = ["_links", "_embedded"]

def build_link(link):
    return { "href": link.href }

def build_links(resource):
    link_dict = {}
    rels = resource.links.get_rels()
    for rel in rels:
        links = resource.links.filter_by_rel(rel)
        if len(links) == 1:
            link_dict[rel] = build_link(links[0])
        else:
            link_dict[rel] = [build_link(link) for link in links]
    return link_dict

def build_resource(resource):
    hal_rep = dict((attr.name, attr.value) for attr in resource.attributes.all())
    hal_rep["_links"] = build_links(resource)
    return hal_rep

def parse_attributes(hal_rep, resource):
    attrs = [[key, value] for key, value in hal_rep.items()
                if key not in RESERVED_ATTRIBUTES]
    for attr in attrs:
        resource.attributes.add(attr[0], attr[1])

def parse_link(rel, link, resource):
    if "templated" in link and link["templated"]:
        return
    return resource.links.add(rel=rel, href=link["href"])

def parse_links(hal_rep, resource):
    if not "_links" in hal_rep or not hal_rep["_links"]:
        return
    for rel, link in hal_rep["_links"].items():
        if type(link) is dict:
            parse_link(rel, link, resource)
        else:
            for item in link:
                parse_link(rel, item, resource)


class HalJSONAdapter(object):

    media_type = "application/hal+json"

    @classmethod
    def build(self, resource):
        hal_rep = build_resource(resource)
        return json.dumps(hal_rep)

    @classmethod
    def parse(self, raw_json):
        hal_rep = json.loads(raw_json)
        resource = Representor()
        parse_attributes(hal_rep, resource)
        parse_links(hal_rep, resource)
        return resource



