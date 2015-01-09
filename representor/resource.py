from .base import Representor
from .adapters.hal_json import HalJSONAdapter

Representor.adapters.add(HalJSONAdapter)
