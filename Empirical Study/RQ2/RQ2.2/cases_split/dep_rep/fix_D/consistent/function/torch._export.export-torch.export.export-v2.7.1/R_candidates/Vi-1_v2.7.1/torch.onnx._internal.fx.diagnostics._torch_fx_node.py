@_format_argument.register
def _torch_fx_node(obj: torch.fx.Node) -> str:
    node_string = f"fx.Node({obj.target})[{obj.op}]:"
    if "val" not in obj.meta:
        return node_string + "None"
    return node_string + format_argument(obj.meta["val"])
