"""Jinja-Like Prompt Template Renderer.
100% Python Standard Library.
"""
import re

class JinjaLikePromptTemplateRenderer:
    """Safe AST-free Jinja-like prompt template parser and renderer."""

    @staticmethod
    def _get_val(context: dict, path: str):
        keys = path.strip().split(".")
        curr = context
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return ""
        return curr

    @classmethod
    def render(cls, template: str, context: dict) -> str:
        for_regex = re.compile(r'\{%\s*for\s+([a-zA-Z0-9_]+)\s+in\s+([a-zA-Z0-9_\.]+)\s*%\}(.*?)\{%\s*endfor\s*%\}', re.DOTALL)
        def replace_for(m):
            var_name, list_path, body = m.groups()
            items = cls._get_val(context, list_path)
            if not isinstance(items, list):
                return ""
            out = []
            for item in items:
                child_ctx = dict(context)
                child_ctx[var_name] = item
                out.append(cls.render(body, child_ctx))
            return "".join(out)

        rendered = for_regex.sub(replace_for, template)

        if_else_regex = re.compile(r'\{%\s*if\s+([a-zA-Z0-9_\.]+)\s*%\}(.*?)(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}', re.DOTALL)
        def replace_if(m):
            cond_var, true_branch, false_branch = m.groups()
            val = cls._get_val(context, cond_var)
            return true_branch if bool(val) else (false_branch or "")

        rendered = if_else_regex.sub(replace_if, rendered)

        var_regex = re.compile(r'\{\{\s*([a-zA-Z0-9_\.]+)\s*\}\}')
        def replace_var(m):
            val = cls._get_val(context, m.group(1))
            return str(val) if val is not None else ""

        return var_regex.sub(replace_var, rendered)
