from inputs import InputCollection
from transitions import TransitionCollectionWrapper, TransitionResource

class QueryCollection(TransitionCollectionWrapper):

    def __init__(self, resource):
        self.item = QueryItem
        self.resource = resource

class QueryItem(TransitionResource):

    def __init__(self, relation_type, uri, **kwargs):
        super(QueryItem, self).__input__(relation_type, uri, **kwargs)
        self.params = InputCollection()
