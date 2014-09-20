__title__ = 'hypermedia_resource'
__version__ = '0.1.3'
__author__ = 'Stephen Mizell'
__license__ = 'MIT'

from base import HypermediaResource
from adapters.hal_json import HalJSONAdapter
from adapters.maze_xml import MazeXMLAdapter

HypermediaResource.adapters.add(HalJSONAdapter)
HypermediaResource.adapters.add(MazeXMLAdapter)
