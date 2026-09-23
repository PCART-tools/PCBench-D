@_format_argument.register
def _torch_fx_graph_module(obj: torch.fx.GraphModule) -> str:
    return f"torch.fx.GraphModule({obj.__class__.__name__})"
