"""MCP stdio server for R-Tree Spatial Index."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import SimpleRTree

tree = SimpleRTree()

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "insert_bounding_box",
                        "description": "Insert item with 2D bounding box [min_x, min_y, max_x, max_y]",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "mbr": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                                "item_id": {"type": "string"}
                            },
                            "required": ["mbr", "item_id"]
                        }
                    },
                    {
                        "name": "query_range",
                        "description": "Query all items intersecting search window [min_x, min_y, max_x, max_y]",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "search_mbr": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4}
                            },
                            "required": ["search_mbr"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "insert_bounding_box":
            mbr = args.get("mbr")
            item = args.get("item_id")
            tree.insert(mbr, item)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "inserted", "total_items": len(tree.entries)}}
        elif name == "query_range":
            smbr = args.get("search_mbr")
            hits = tree.query(smbr)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"hits": hits, "count": len(hits)}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
