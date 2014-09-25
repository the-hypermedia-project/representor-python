from .dom import ItemCollection

class MediaTypeCollection(ItemCollection):

    def __init__(self):
        super(MediaTypeCollection, self).__init__()
        self.item = MediaTypeItem

class MediaTypeItem(object):

    def __init__(self, media_type, **kwargs):
        self.media_type = media_type
