from negotiator import ContentNegotiator, AcceptParameters, ContentType
from .resource import HypermediaResource

try:
    from flask import Response
except:
    pass

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

class APIResource(object):

    def default_type(self):
        return "application/hal+json"

    def available_actions(self):
        return [action for action in self.actions().values()
            if hasattr(self, action)]

    def available_methods(self):
        return [method for method, action in self.actions().items()
            if action in self.available_actions()]

    def method_override(self):
        return "_method"

    def actions(self):
        """Defaults Actions"""
        return {
            'GET': 'read',
            'POST': 'process',
            'PATCH': 'partial',
            'PUT': 'save',
            'DELETE': 'remove'
        }

    def build_response(self, resource, accepts):
        response_builder = ResponseBuilder(self.default_type())
        return response_builder.build(resource, accepts)

class FlaskAPIResource(APIResource):

    def flask_response(self, resource, request, *args, **kwargs):
        response = self.build_response(resource, request.headers.get('Accept'))
        return Response(response.body, mimetype=response.media_type, *args, **kwargs)

    def get_method(self, request):
        if request.method != "POST":
            return request.method
        method_override = self.method_override()
        if request.form.has_key(method_override) and request.method == "POST":
            return request.form[method_override]
        return request.method

    def response_for(self, request):
        method = self.get_method(request)
        action_name = self.actions()[method]
        action = getattr(self, action_name)
        return action(request)
