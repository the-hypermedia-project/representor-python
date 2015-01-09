Hypermedia Representor - Python
-------------------------------

[![Build Status](http://img.shields.io/travis/the-hypermedia-project/representor-python/master.svg?style=flat)](https://travis-ci.org/the-hypermedia-project/representor-python)

This library provides a generic interface for hypermedia messages. It is currently in active development and is not recommended for production use.

## Installing

```
python setup.py install
```

## Usage

### Representor

```python
from representor import Representor

representor = Representor()

# Adding representor attributes
representor.attributes.add("name", "John Doe")
representor.attributes.add("email", "john@example.com")

# Retreiving attributes
name_attr = representor.attributes.get("name")
name_attr.value

# Adding links
representor.links.add("self", "/customers/1")
representor.links.add("orders", "/customers/1/orders")

# Adding meta data
representor.meta.attributes.add("title", "Customer Details")
representor.meta.links.add("profile", "http://example.com/customer_profile")

# Finding links and transitions
has_self = representor.transitions.has_rel("self") # True
self_link = representor.transitions.get("self")
profile_link = representor.meta.links.get("profile")

# Translate to media types
hal = representor.translate_to("application/hal+json")

# Translate from media types
hal_json = '{ "_links": { "self": { "href": "/example" }}}'
new_representor = Representor.translate_from("application/hal+json", hal_json)
```

#### Supported Media Types

* HAL+JSON
* Maze+XML

### Adding Adapters

```python
from representor import Representor
from representor.contrib.browser import BrowserAdapter

# Add the adapter
Representor.adapters.add(BrowserAdapter)
```

#### Contrib Adapters

These are adapters that are not considered to be part of the defaults, but are added in the library for easy access.

##### Browser

This is an adapter that can be used to build HTML representations of a resource. This is only used for building and will not be made to parse HTML.

To use:

```python
from representor.contrib.browser import BrowserAdapter
Representor.adapters.add(BrowserAdapter)
```

### HypermediaResponse

A Hypermedia Response can be used to automatically generate a representation based on what the client accepts. It uses content negotiation to decide the type based on what adapters have been added to the `Representor` adapters, either by default or manually.

```python
from representor import Representor
from representor.wrappers import HypermediaResponse, ResponseBuilder

# The resource
representor = Representor()
representor.links.add("self", "/example")

# What the client accepts, which is used for content negotiation
accepts = "application/hal+json"

# New builder with default type
response_builder = ResponseBuilder("application/hal+json")
response = response_builder.build(representor, accepts)

# Fields for response
response.media_type # The media type of the response
response.body # The body of the response
```

More detailed docs to come as this API is developed.

## Running Tests

```script
python setup.py test
```
