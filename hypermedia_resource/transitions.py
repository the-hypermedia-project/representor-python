from attributes import AttributeCollection
from base import Collection
from inputs import InputCollection
from media_types import MediaTypeCollection
from meta import MetaItem
from semantics import Semantics
from types_of import TypesOfCollection
from utils import filter_by_type

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
        if self.method in safe
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
