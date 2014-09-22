Hypermedia Resource - Python
----------------------------

This library provides a generic interface for hypermedia messages. It is currently in active development and is not recommended for production use. 

## Installing

```
python setup.py install
```

## Usage

### HypermediaResource

```python
from hypermedia_resource import HypermediaResource

resource = HypermediaResource()

# Adding resource attributes
resource.attributes.add("name", "John Doe")
resource.attributes.add("email", "john@example.com")

# Retreiving attributes
name_attr = resource.attributes.get("name")
name_attr.value

# Adding links
resource.links.add("self", "/customers/1")
resource.links.add("orders", "/customers/1/orders")

# Adding meta data
resource.meta.attributes.add("title", "Customer Details")
resource.meta.links.add("profile", "http://example.com/customer_profile")

# Finding links and transitions
has_self = resource.transitions.has_rel("self") # True
self_link = resource.transitions.get("self")
profile_link = resource.meta.links.get("profile")

# Translate to media types
hal = resource.translate_to("application/hal+json")

# Translate from media types
hal_json = '{ "_links": { "self": { "href": "/example" }}}'
new_resource =HypermediaResource.translate_from("application/hal+json", hal_json)
```

#### Supported Media Types

* HAL+JSON
* Maze+XML

### Adding Adapters

```python
from hypermedia_resource import HypermediaResource
from hypermedia_resource.contrib.browser import BrowserAdapter

# Add the adapter
HypermediaResource.adapters.add(BrowserAdapter)
```

#### Contrib Adapters

These are adapters that are not considered to be part of the defaults, but are added in the library for easy access.

##### Browser

This is an adapter that can be used to build HTML representations of a resource. This is only used for building and will not be made to parse HTML.

To use:

```python
from hypermedia_resource.contrib.browser import BrowserAdapter
HypermediaResource.adapters.add(BrowserAdapter)
```

### HypermediaResponse

A Hypermedia Response can be used to automatically generate a representation based on what the client accepts. It uses content negotiation to decide the type based on what adapters have been added to the `HypermediaResource` adapters, either by default or manually.

```python
from hypermedia_resource import HypermediaResource
from hypermedia_resource.wrappers import HypermediaResponse, ResponseBuilder

# The resource
resource = HypermediaResource()
resource.links.add("self", "/example")

# What the client accepts, which is used for content negotiation
accepts = "application/hal+json"

# New builder with default type
response_builder = ResponseBuilder("application/hal+json")
response = response_builder.build(resource, accepts)

# Fields for response
response.media_type # The media type of the response
response.body # The body of the response
```

More detailed docs to come as this API is developed.

## Running Tests

```script
python setup.py test
```