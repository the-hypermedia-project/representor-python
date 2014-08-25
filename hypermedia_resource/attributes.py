from base import Collection
from semantics import Semantics

class AttributeCollection(Collection):

    def __init__(self):
        self.item = AttributeItem

class AttributeItem(Semantics):

    def __init__(self, name, value=None, **kwargs):
        self.name = name
        self.value = value
