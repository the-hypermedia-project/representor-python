from inputs import InputCollection
from media_types import MediaTypeCollection
from transitions import BaseTransitionItem, TransitionCollectionWrapper

class ActionCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = ActionItem
        self.resource = resource

class ActionItem(BaseTransitionItem):

    def __init__(self, relation_type, uri, method, **kwargs):
        super(ActionItem, self).__init__(relation_type, uri, method **kwargs)
        self.request_types = MediaTypeCollection()
