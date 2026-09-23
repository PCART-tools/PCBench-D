def _fx_node_to_onnx_message_formatter(
    fn: Callable,
    self,
    node: torch.fx.Node,
    *args,
    **kwargs,
) -> str:
    return f"FX Node: {node.op}:{node.target}[name={node.name}]. "
