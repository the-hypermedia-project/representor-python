try:
    from jinja2 import Template
except:
    pass

class BrowserAdapter(object):

    media_type = "text/html"

    @classmethod
    def build(self, resource):
        template = Template(resource_template)
        return template.render(main_resource=resource)

resource_template = """
{% macro resource_markup(resource, embedded=False) %}
    {% if embedded %}
        <div class="page-header">
            {% if resource.meta.attributes.has("title") %}
                <h1>{{ resource.meta.attributes.get("title").value }}</h1>
            {% else %}
                <h1>Embedded: {{ resource.rel }}</h1>
            {% endif %}
        </div>
    {% else %}
        <div class="page-header">
            {% if resource.meta.attributes.has("title") %}
                <h1>{{ resource.meta.attributes.get("title").value }}</h1>
            {% else %}
                <h1>Hypermedia Browser</h1>
            {% endif %}
        </div>
    {% endif %}

    {% if resource.attributes.all() %}
        <div class="page-header">
            <h2>Attributes</h2>
        </div>
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
        <div class="page-header">
            <h2>Links</h2>
        </div>
        <ul class="nav nav-pills nav-stacked">
            {% for link in resource.links.all() %}
                {% if link.label %}
                    <li><a href="{{ link.href }}" rel="{{ link.rel }}">{{ link.label }}</a></li>
                {% else %}
                    <li><a href="{{ link.href }}" rel="{{ link.rel }}">{{ link.rel }}</a></li>
                {% endif %}
            {% endfor %}
        </ul>
    {% endif %}

    {% if resource.queries.all() %}
        <div class="page-header">
            <h2>Queries</h2>
        </div>
        {% for query in resource.queries.all() %}
            {% if query.label %}
                <h3>{{ query.label }}</h3>
            {% endif %}
            {{ form("GET", query.href, query.params.all()) }}
        {% endfor %}
    {% endif %}

    {% if resource.actions.all() %}
        <div class="page-header">
            <h2>Actions</h2>
        </div>
        {% for action in resource.actions.all() %}
            {% if action.label %}
                <h3>{{ action.label }}</h3>
            {% endif %}
            {{ form(action.method, action.href, action.attributes.all()) }}
        {% endfor %}
    {% endif %}

    {% if resource.embedded_resources.all() %}
        {% for embedded_resource in resource.embedded_resources.all() %}
            <div class="embedded">
                {{ resource_markup(embedded_resource, True) }}
            </div>
        {% endfor %}
    {% endif %}
{% endmacro %}

{% macro form(method, action, params) %}
    {% if method in ['GET', 'POST'] %}
        <form method="{{ method }}" action="{{ action }}" class="form">
    {% else %}
        <form method="POST" action="{{ action }}" class="form">
        <input type="hidden" name="_method" value="{{ method }}" />
    {% endif %}
        {% for param in params %}
            <div class="form-group">
                <label>{{ param.name }}</label>
                {% if param.options.all() %}
                    {{ select(param) }}
                {% else %}
                    {{ input(param) }}
                {% endif %}
            </div>
        {% endfor %}
        <input type="submit" class="btn" />
    </form>
{% endmacro %}

{% macro input(param) %}
    <input type="text"
           name="{{ param.name }}" {% if param.value %}value="{{ param.value }}"{% endif %}
           class="form-control" />
{% endmacro %}

{% macro select(param) %}
    <select name="{{ param.name }}" class="form-control">
        {% for option in param.options.all() %}
            <option {% if option.value == param.value %} selected="selected"{% endif %} value="{{ option.value }}">{{ option.name }}</option>
        {% endfor %}
    </select>
{% endmacro %}

<!doctype html>
<html>
    <head>
        {% if main_resource.meta.attributes.has("title") %}
            <title>{{ main_resource.meta.attributes.get("title").value }}</title>
        {% else %}
            <title>Hypermedia Browser</title>
        {% endif %}
        <link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
        <style>
        body { margin-bottom: 40px; }
        .main { max-width: 800px; }
        .embedded {
            padding-left: 15px;
            border-left: 2px solid #2980B9;
        }
        </style>
    </head>
    <body>
        <div class="container-fluid main">
            {{ resource_markup(main_resource) }}
        </div>
    </body>
</html>
"""
