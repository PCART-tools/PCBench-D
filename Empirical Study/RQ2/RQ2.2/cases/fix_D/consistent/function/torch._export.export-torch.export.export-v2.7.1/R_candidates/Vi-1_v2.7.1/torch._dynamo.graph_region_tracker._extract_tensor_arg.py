def _extract_tensor_arg(arg: Any) -> Any:
    if isinstance(arg, Node):
        return arg.meta.get("example_value")
    else:
        return None
