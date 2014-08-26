from dom import Collection
from semantics import Semantics

class AttributeCollection(Collection):

    def __init__(self):
        super(AttributeCollection, self).__init__()
        self.item = AttributeItem

    def filter_by_name(self, name):
        return [item for item in self._items if item.name == name]

    def get(self, name):
        items = self.filter_by_name(name)
        return items[0]

class AttributeItem(Semantics):

    def __init__(self, name, value=None, **kwargs):
        self.name = name
        self.value = value
