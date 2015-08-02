class Collection(object):

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def append(self, item):
        self._items.append(item)

    def add(self, *args):
        for item in args:
            self.append(item)

    def all(self):
        return self._items

    def set_items(self, items):
        self._items = items

class ItemCollection(Collection):

    def __init__(self, item=None):
        super(ItemCollection, self).__init__()
        self.item = item

    def set_item_type(self, item):
        self.item = item

    def add(self, *args, **kwargs):
        new_item = self.item(*args, **kwargs)
        self.append(new_item)
        return new_item

    def filter_by(self, attr, value):
        return [item for item in self.all() if getattr(item, attr) == value]

class Item(object):

    def __init__(self, *args, **kwargs):
        pass

    def set(self, name, value):
        setattr(self, name, value)
