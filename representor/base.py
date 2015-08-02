from .attributes import AttributeCollection
from .dom import Collection, ItemCollection
from .inputs import InputCollection
from .media_types import MediaTypeCollection
from .translator import Translator
from .utils import filter_by_type

class TranslatorMixin(object):

    adapters = Translator()

    def translate_to(self, media_type):
        return self.adapters.translate_to(media_type, self)

    @classmethod
    def translate_from(self, media_type, raw_representation):
        return self.adapters.translate_from(media_type, raw_representation)

    @classmethod
    def reset_adapters(self):
        Representor.adapters = Translator()

class Representor(TranslatorMixin):

    def __init__(self, *args, **kwargs):
        self.href = kwargs.get('href', None)
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
        return [item for item in self.all() if item.rel == rel]

    def get(self, rel):
        items = self.filter_by_rel(rel)
        return items[0]

    def get_rels(self):
        return [item.rel for item in self.all()]

class BaseTransitionItem(object):

    def __init__(self, rel, method='GET', **kwargs):
        self.rel = rel
        self.method = method
        self.hreflang = kwargs.get('hreflang', None)
        self.embed_as = kwargs.get('embed_as', None)
        self.response_types = MediaTypeCollection()
        self.label = kwargs.get('label', None)

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

class TransitionItem(BaseTransitionItem, Representor):

    def __init__(self, rel, href, method='GET', **kwargs):
        Representor.__init__(self, href=href, **kwargs)
        BaseTransitionItem.__init__(self, rel, method, **kwargs)

class TransitionCollectionWrapper(ItemCollection):

    def __init__(self, item=None, resource=None):
        super(TransitionCollectionWrapper, self).__init__()
        self.item = item
        self.resource = resource

    def append(self, item):
        self.resource.transitions.append(item)

    def add(self, rel, href, method='GET', **kwargs):
        new_item = self.item(rel, href, method, **kwargs)
        self.resource.transitions.add(new_item)
        return new_item

    def all(self):
        return filter_by_type(self.resource.transitions.all(), self.item)

    def filter_by_rel(self, rel):
        return [item for item in self.all() if item.rel == rel]

    def get(self, rel):
        items = self.filter_by_rel(rel)
        return items[0]

    def get_rels(self):
        return [item.rel for item in self.all()]

    def has_rel(self, rel):
        return rel in self.get_rels()

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
        super(ActionItem, self).__init__(rel, method, **kwargs)
        self.href = href
        self.meta = MetaItem(self)
        self.request_types = MediaTypeCollection()
        self.attributes = InputCollection()

class LinkCollection(TransitionCollectionWrapper):

    def __init__(self, resource=None):
        super(LinkCollection, self).__init__()
        self.item = LinkItem
        self.resource = resource

    def add(self, rel, href, **kwargs):
        return super(LinkCollection, self).add(rel, href, 'GET', **kwargs)

class LinkItem(TransitionItem):
    pass

class QueryCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = QueryItem
        self.resource = resource

    def add(self, rel, href, **kwargs):
        return super(QueryCollection, self).add(rel, href, 'GET', **kwargs)

class QueryItem(TransitionItem):

    def __init__(self, rel, href, method, **kwargs):
        super(QueryItem, self).__init__(rel, href, method, **kwargs)
        self.params = InputCollection()

class EmbeddedResourceCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = EmbeddedResourceItem
        self.resource = resource

class EmbeddedResourceItem(TransitionItem):
    pass
