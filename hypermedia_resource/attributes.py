from .dom import ItemCollection

class AttributeCollection(ItemCollection):

    def __init__(self):
        super(AttributeCollection, self).__init__()
        self.item = AttributeItem

    def filter_by_name(self, name):
        return [item for item in self._items if item.name == name]

    def get(self, name):
        items = self.filter_by_name(name)
        return items[0]

    def has(self, name):
        return len(self.filter_by_name(name)) > 0

class AttributeItem(object):

    def __init__(self, name, value=None, **kwargs):
        self.label = kwargs.get("label", None)
        self.name = name
        self.value = value
