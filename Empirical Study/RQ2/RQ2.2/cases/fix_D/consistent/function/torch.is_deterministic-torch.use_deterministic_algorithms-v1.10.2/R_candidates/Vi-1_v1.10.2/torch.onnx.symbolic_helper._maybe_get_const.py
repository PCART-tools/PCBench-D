def _maybe_get_const(value, desc):
    if _is_value(value) and value.node().kind() == "onnx::Constant":
        return _parse_arg(value, desc)
    return value
