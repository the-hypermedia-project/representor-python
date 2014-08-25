from base import Collection

class MediaTypeCollection(Collection):

    def __init__(self):
        self.item = MediaTypeItem

class MediaTypeItem:

    def __init__(self, media_type, **kwargs):
        self.media_type = media_type
