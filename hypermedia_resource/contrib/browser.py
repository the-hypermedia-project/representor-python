try:
    from jinja2 import Template
except:
    pass

resource_template = """
<html>
    <head>
        {% if resource.meta.attributes.has("title") %}
            <title>{{ resource.meta.attributes.get("title").value }}</title>
        {% else %}
            <title>Hypermedia Browser</title>
        {% endif %}
        <link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container-fluid">
            {% if resource.meta.attributes.has("title") %}
                <h1>{{ resource.meta.attributes.get("title").value }}</h1>
            {% else %}
                <h1>Hypermedia Browser</h1>
            {% endif %}
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
            </div>
        </div>
    </body
</html>
"""

class BrowserAdapter(object):

    media_type = "text/html"

    @classmethod
    def build(self, resource):
        template = Template(resource_template)
        return template.render(resource=resource)
