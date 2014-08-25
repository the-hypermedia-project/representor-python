from base import BaseHypermediaResource
from transitions import TransitionCollectionWrapper, TransitionItem

class LinkCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = LinkItem
        self.resource = resource

class LinkItem(TransitionItem):
    pass

