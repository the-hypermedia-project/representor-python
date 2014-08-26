from dom import Collection

class Semantics(object):

    def __init__(self, **kwargs):
        self.label = kwargs.get('label', None)
        self.types_of = TypesOfCollection()

class TypesOfCollection(Collection):

    def __init__(self):
        self.item = TypesOfItem

class TypesOfItem(object):

    def __init__(self, type_of, **kwargs):
        self.type_of = type_of
