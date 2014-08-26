from attributes import AttributeCollection
from dom import Collection
from inputs import InputCollection
from media_types import MediaTypeCollection
from semantics import Semantics
from utils import filter_by_type

class TranslatiorMixin:

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

class HypermediaResource(Semantics, TranslatiorMixin):

    def __init__(self, *args, **kwargs):
        super(HypermediaResource, self).__init__(**kwargs)
        self.meta = MetaItem(self)
        self.attributes = AttributeCollection()
        self.transitions = TransitionCollection()

        # These are all types of transitions
        self.links = LinkCollection(self)
        self.queries = QueryCollection(self)
        self.actions = ActionCollection(self)
        self.embedded_resources = EmbeddedResourceCollection(self)

class TransitionCollection(Collection):

    def __init__(self):
        super(TransitionCollection, self).__init__()
        self.item = TransitionItem

    def filter_by_rel(self, rel):
        return [item for item in self._items if item.rel == rel]

    def get(self, rel):
        items = self.filter_by_rel(rel)
        return items[0]

class BaseTransitionItem(Semantics):

    def __init__(self, rel, href, method='GET', **kwargs):
        super(BaseTransitionItem, self).__init__()
        self.rel = rel
        self.href = href
        self.method = method
        self.embed_as = kwargs.get('embed_as', None)
        self.language = kwargs.get('language', None)
        self.response_types = MediaTypeCollection()

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

class TransitionItem(BaseTransitionItem, HypermediaResource):

    def __init__(self, rel, href, method='GET', **kwargs):
        HypermediaResource.__init__(self, **kwargs)
        BaseTransitionItem.__init__(self, rel, href, method, **kwargs)

class TransitionCollectionWrapper(Collection):

    def __init__(self, item=None, resource=None):
        super(TransitionCollectionWrapper, self).__init__()
        self.item = item
        self.resource = resource

    def append(self, item):
        self.resource.transitions.append(item)

    def add(self, rel, href, method='GET', **kwargs):
        new_item = self.item(rel, href, method, **kwargs)
        self.resource.transitions.append(new_item)
        return new_item

    def all(self):
        return filter_by_type(self.resource.transitions.all(), self.item)

    def filter_by_rel(self, rel):
        return [item for item in self.resource.transitions._items if item.rel == rel]

    def get(self, rel):
        items = self.filter_by_rel(rel)
        return items[0]

class MetaItem(object):

    def __init__(self, resource):
        self.attributes = AttributeCollection()
        self.links = LinkCollection(resource)

class ActionCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = ActionItem
        self.resource = resource

class ActionItem(BaseTransitionItem):

    def __init__(self, rel, href, method, **kwargs):
        super(ActionItem, self).__init__(rel, href, method **kwargs)
        self.request_types = MediaTypeCollection()
        self.attributes = InputCollection()

class LinkCollection(TransitionCollectionWrapper):

    def __init__(self, resource=None):
        super(LinkCollection, self).__init__()
        self.item = LinkItem
        self.resource = resource

class LinkItem(TransitionItem):
    pass

class QueryCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = QueryItem
        self.resource = resource

class QueryItem(TransitionItem):

    def __init__(self, rel, href, **kwargs):
        super(QueryItem, self).__input__(rel, href, **kwargs)
        self.params = InputCollection()

class EmbeddedResourceCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = EmbeddedResourceItem
        self.resource = resource

class EmbeddedResourceItem(TransitionItem):
    pass
