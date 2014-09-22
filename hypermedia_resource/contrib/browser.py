try:
    from jinja2 import Template
except:
    pass

class BrowserAdapter(object):

    media_type = "text/html"

    @classmethod
    def build(self, resource):
        template = Template(resource_template)
        return template.render(resource=resource)

resource_template = """
{% macro resource_markup(resource) %}
    {% if resource.meta.attributes.has("title") %}
        <h1>{{ resource.meta.attributes.get("title").value }}</h1>
    {% else %}
        <h1>Hypermedia Browser</h1>
    {% endif %}

    {% if resource.attributes.all() %}
        <h2>Attributes</h2>
        <dl class="dl-horizontal attributes">
            {% for attr in resource.attributes.all() %}
                {% if attr.label %}
                    <dt>{{ attr.label }}</dt>
                {% else %}
                    <dt>{{ attr.name }}</dt>
                {% endif %}
                <dd>{{ attr.value }}</dd>
            {% endfor %}
        </dl>
    {% endif %}

    {% if resource.links.all() %}
        <h2>Links</h2>
        <ul class="links">
            {% for link in resource.links.all() %}
                <li>
                {% if link.label %}
                    <a href="{{ link.href }}" rel="{{ link.rel }}">{{ link.label }}</a>
                {% else %}
                    <a href="{{ link.href }}" rel="{{ link.rel }}">{{ link.rel }}</a>
                {% endif %}
                </li>
            {% endfor %}
        </ul>
    {% endif %}

    {% if resource.queries.all() %}
        <h2>Queries</h2>
        {% for query in resource.queries.all() %}
            {{ form("GET", query.href, query.params.all()) }}
        {% endfor %}
    {% endif %}
{% endmacro %}

{% macro form(method, action, params) %}
    <form method="{{ method }}" action="{{ action }}" class="form">
        {% for param in params %}
            <div class="form-group">
                <label>{{ param.name }}</label>
                {% if param.value %}
                    <input type="text" name="{{ param.name }}" value="{{ param.value }}" class="form-control" />
                {% else %}
                    <input type="text" name="{{ param.name }}" class="form-control" />
                {% endif %}
            </div>
        {% endfor %}
    </form>
{% endmacro %}

<!doctype html>
<html>
    <head>
        {% if resource.meta.attributes.has("title") %}
            <title>{{ resource.meta.attributes.get("title").value }}</title>
        {% else %}
            <title>Hypermedia Browser</title>
        {% endif %}
        <link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
        <style>
        .main { max-width: 800px; }
        </style>
    </head>
    <body>
        <div class="container-fluid main">
            {{ resource_markup(resource) }}
        </div>
    </body>
</html>
"""
