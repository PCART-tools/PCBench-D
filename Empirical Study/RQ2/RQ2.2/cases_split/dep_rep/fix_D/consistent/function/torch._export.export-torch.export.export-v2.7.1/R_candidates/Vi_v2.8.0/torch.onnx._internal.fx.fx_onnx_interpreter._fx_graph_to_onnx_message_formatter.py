def _fx_graph_to_onnx_message_formatter(
    fn: Callable,
    self,
    fx_graph_module: torch.fx.GraphModule,
    *args,
    **kwargs,
) -> str:
    return f"FX Graph: {fx_graph_module._get_name()}. "
