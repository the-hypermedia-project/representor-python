from negotiator import ContentNegotiator, AcceptParameters, ContentType
from .resource import HypermediaResource

class HypermediaResponse(object):

    def __init__(self, media_type, resource):
        self.media_type = media_type
        self.body = resource.translate_to(media_type)

class ResponseBuilder(object):

    def __init__(self, default_type):
        self.default_type = default_type

    def build(self, resource, accept):
        adapters = HypermediaResource.adapters.all()
        acceptable = [AcceptParameters(ContentType(adapter.media_type)) for adapter in adapters]
        cn = ContentNegotiator(AcceptParameters(ContentType(self.default_type)), acceptable)
        negotiate = cn.negotiate(accept=accept)
        if negotiate:
            return HypermediaResponse(str(negotiate.content_type), resource)
        return HypermediaResponse(self.default_type, resource)
