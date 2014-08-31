Hypermedia Resource - Python
----------------------------

This library provides a generic interface for hypermedia messages. It is currently in active development and is not recommended for production use. 

## Installing

```
python setup.py install
```

## Usage

```python
resource = HypermediaResource()

# Adding resource attributes
resource.attributes.add('name', 'John Doe')
resource.attributes.add('email', 'john@example.com')

# Retreiving attributes
name_attr = resource.attributes.get('name')

# Adding transitions
resource.transitions.add('self', '/customers/1')
resource.transitions.add('orders', '/customers/1/orders')

# Adding meta data
resource.meta.attributes.add('title', 'Customer Details')
resource.meta.links.add('profile', 'http://example.com/customer_profile')

# Finding links and transitions
self_link = resource.transitions.get_by_rel('self')
profile_link = resource.meta.links.get_by_rel('profile')
```

More to come as this API is developed.