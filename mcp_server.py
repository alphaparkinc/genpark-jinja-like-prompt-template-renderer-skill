"""MCP Server for Jinja-Like Prompt Template Renderer.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import JinjaLikePromptTemplateRenderer

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "render_template",
                                "description": "Render safe Jinja-like prompt template with variables, loops, and conditionals",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "template": {"type": "string"},
                                        "context": {"type": "object"}
                                    },
                                    "required": ["template", "context"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                out = JinjaLikePromptTemplateRenderer.render(args.get("template", ""), args.get("context", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": out}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
