from .base import HypermediaResource
from .adapters.hal_json import HalJSONAdapter
from .adapters.maze_xml import MazeXMLAdapter

HypermediaResource.adapters.add(HalJSONAdapter)
HypermediaResource.adapters.add(MazeXMLAdapter)
