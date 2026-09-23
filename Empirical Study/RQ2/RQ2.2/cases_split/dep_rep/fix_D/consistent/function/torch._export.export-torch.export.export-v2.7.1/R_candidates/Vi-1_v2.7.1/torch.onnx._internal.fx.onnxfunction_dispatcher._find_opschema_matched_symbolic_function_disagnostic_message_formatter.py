def _find_opschema_matched_symbolic_function_disagnostic_message_formatter(
    fn: Callable,
    self,
    node: torch.fx.Node,
    default_and_custom_functions: list[registration.ONNXFunction],
    *args,
    **kwargs,
) -> str:
    """Format the diagnostic message for the nearest match warning."""
    all_function_overload_names = ""
    for symbolic_func in default_and_custom_functions:
        overload_func = symbolic_func.onnx_function
        all_function_overload_names += f"ONNX Node: {overload_func.name}[opset={overload_func.opset};is_custom={symbolic_func.is_custom}]. \n"  # noqa: B950
    return f"FX Node: {node.target}. \n{all_function_overload_names}"
