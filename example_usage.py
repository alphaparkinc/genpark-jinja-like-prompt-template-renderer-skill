"""Example usage for Jinja-Like Prompt Template Renderer."""
from client import JinjaLikePromptTemplateRenderer

template = """You are an assistant for {{ organization.name }}.
{% if is_admin %}
You have root administrative privileges.
{% else %}
Standard user role assigned.
{% endif %}
Active Tools:
{% for t in tools %}
- {{ t.name }}: {{ t.description }}
{% endfor %}
"""

ctx = {
    "organization": {"name": "GenPark AI"},
    "is_admin": True,
    "tools": [
        {"name": "web_search", "description": "Search the live web"},
        {"name": "code_exec", "description": "Run sandboxed Python"}
    ]
}

res = JinjaLikePromptTemplateRenderer.render(template, ctx)
print(res)
