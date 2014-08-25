from transitions import TransitionItem

class EmbeddedResourceCollection(TransitionTypeCollection):

    def __init__(self, resource):
        self.item = EmbeddedResourceItem
        self.resource = resource

class EmbeddedResourceItem(TransitionItem):
    pass
