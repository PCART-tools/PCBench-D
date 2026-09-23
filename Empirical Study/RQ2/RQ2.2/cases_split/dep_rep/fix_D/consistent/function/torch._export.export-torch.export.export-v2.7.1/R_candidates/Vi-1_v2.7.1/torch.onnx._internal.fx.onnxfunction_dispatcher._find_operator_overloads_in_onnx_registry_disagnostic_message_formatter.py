def _find_operator_overloads_in_onnx_registry_disagnostic_message_formatter(
    fn: Callable,
    self,
    node: torch.fx.Node,
    *args,
    **kwargs,
) -> str:
    """Format the diagnostic message for the nearest match warning."""
    return f"Searching operator overload: '{node.target}' in onnx registry...\n"
