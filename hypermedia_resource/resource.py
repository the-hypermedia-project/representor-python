from .base import HypermediaResource
from .adapters.hal_json import HalJSONAdapter

HypermediaResource.adapters.add(HalJSONAdapter)
