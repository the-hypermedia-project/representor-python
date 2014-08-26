class Collection(object):

    def __init__(self, item=None):
        self._items = []
        self.item = item

    def append(self, item):
        self._items.append(item)

    def add(self, *args, **kwargs):
        new_item = self.item(*args, **kwargs)
        self.append(new_item)
        return new_item

    def all(self):
        return self._items

class Item(object):
    pass
