import json
from hypermedia_resource import HypermediaResource

class HalJSONAdapter(object):

    media_type = "application/hal+json"

    @classmethod
    def build(self, resource):
        hal_rep = dict((attr.name, attr.value)
            for attr in resource.attributes.all())
        return json.dumps(hal_rep)


