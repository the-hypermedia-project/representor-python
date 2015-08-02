from .dom import Collection

class Translator(Collection):

    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__()
        for adapter in args:
            self.add(adapter)

    def register(self, adapter):
        self.add(adapter)

    def get(self, media_type):
        return [adapter for adapter in self.all() if adapter.media_type == media_type][0]

    def get_media_types(self):
        return [adapter.media_type for adapter in self.all()]

    def translate_from(self, media_type, raw_representation):
        adapter = self.get(media_type)
        return adapter.parse(raw_representation)

    def translate_to(self, media_type, resource):
        adapter = self.get(media_type)
        return adapter.build(resource)
