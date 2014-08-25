from actions import ActionCollection
from attributes import AttributeCollection
from embedded_resources import EmbeddedResourceCollection
from links import LinkCollection
from meta import MetaItem
from queries import QueryCollection
from semantics import Semantics
from transitions import TransitionCollection

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
            'transitions': self.transitions.to_array(),
            'label': self.label,
            'types_of': self.types_of.to_array()
        }

class Collection:

    def __init__(self):
        self._items = []
        self.item = None

    def append(self, item):
        self._items.append(item)

    def add(self, *args, **kwargs):
        new_item = self.item(*args, **kwargs)
        self.add_item(new_item)
        return new_item

    def all(self):
        return self._items

    def to_array(self):
        return [item.to_dict() for item in self._items]
