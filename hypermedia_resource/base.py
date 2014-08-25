from attributes import AttributeCollection
from dom import Collection
from inputs import InputCollection
from media_types import MediaTypeCollection
from semantics import Semantics
from utils import filter_by_type

class TranslatorMixin:

    _adapters = {}

    @classmethod
    def register(self, adapter):
        self._adapters[adapter.media_type] = adapter

    @classmethod
    def translate_from(self, media_type, raw_representation):
        adapter = self.adapters[media_type](adapters=self.adapters)
        return adapter.parse(raw_representation)

    def translate_to(self, media_type):
        adapter = self.adapters[media_type]()
        return adapter.build(self)

class HypermediaResource(Semantics):

    def __init__(self, *args, **kwargs):
        super(HypermediaResource, self).__init__(**kwargs)
        self.meta = MetaItem()
        self.attributes = AttributeCollection()
        self.transitions = TransitionCollection()

        # These are all types of transitions
        self.links = LinkCollection(self)
        self.queries = QueryCollection(self)
        self.actions = ActionCollection(self)
        self.embedded_resources = EmbeddedResourceCollection(self)

    def to_dict(self):
        return {
            'meta': self.meta.to_dict(),
            'attributes': self.attributes.to_array(),
            'links': self.links.to_array(),
            'queries': self.queries.to_array(),
            'actions': self.links.to_array(),
            'embedded_resources': self.embedded_resources.to_array(),
            'label': self.label,
            'types_of': self.types_of.to_array()
        }

class TransitionCollection(Collection):

    def add(self, relation_type, uri, method='GET', **kwargs):
        trasition = TransitionItem(relation_type, method, **kwargs)
        self.add_item(trasition)
        return trasition

class BaseTransitionItem(Semantics):

    def __init__(self, relation_type, uri, method='GET', **kwargs):
        super(BaseTransitionItem, self).__init__()
        self.relation_type = relation_type
        self.uri = uri
        self.method = method
        self.embed_as = kwargs.get('embed_as', None)
        self.language = kwargs.get('language', None)
        self.response_types = MediaTypeCollection()
        self.attributes = self.get_attributes()

    @property
    def safe(self):
        safe = ['GET', 'OPTIONS', 'HEAD']
        if self.method in safe:
            return True
        return False

    @property
    def idempotent(self):
        non_idempotent = ['POST', 'PATCH']
        if self.method in non_idempotent:
            return False
        return True

    @property
    def mutable(self):
        if self.method == 'GET':
            return False
        return True

    @property
    def transclude(self):
        if self.embed_as:
            return True
        return False

    def get_attributes(self):
        if self.mutable:
            return InputCollection()
        return AttributeCollection()

class TransitionItem(BaseTransitionItem, HypermediaResource):

    def __init__(self, relation_type, uri, method='GET', **kwargs):
        HypermediaResource.__init__(self, **kwargs)
        BaseTransitionItem.__init__(self, relation_type, uri, method, **kwargs)

class TransitionCollectionWrapper(Collection):

    def __init__(self, item=None, resource=None):
        self.item = item
        self.resource = resource

    def append(self, item):
        self.resource.transitions.append(item)

    def add(self, relation_type, uri, method, **kwargs):
        new_item = self.item(relation_type, method, **kwargs)
        self.resource.transitions.append(new_item)
        return new_item

    def all(self):
        return filter_by_type(self.resource.transitions.all(), self.item)

class MetaItem:

    def __init__(self):
        self.attributes = AttributeCollection()
        self.links = LinkCollection()

class ActionCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = ActionItem
        self.resource = resource

class ActionItem(BaseTransitionItem):

    def __init__(self, relation_type, uri, method, **kwargs):
        super(ActionItem, self).__init__(relation_type, uri, method **kwargs)
        self.request_types = MediaTypeCollection()

class LinkCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = LinkItem
        self.resource = resource

class LinkItem(TransitionItem):
    pass

class QueryCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = QueryItem
        self.resource = resource

class QueryItem(TransitionItem):

    def __init__(self, relation_type, uri, **kwargs):
        super(QueryItem, self).__input__(relation_type, uri, **kwargs)
        self.params = InputCollection()

class EmbeddedResourceCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = EmbeddedResourceItem
        self.resource = resource

class EmbeddedResourceItem(TransitionItem):
    pass
