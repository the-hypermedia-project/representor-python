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
