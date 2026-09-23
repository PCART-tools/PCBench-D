def _avgpool_helper(tuple_fn, padding, kernel_size, stride, divisor_override, name):
    if divisor_override and divisor_override.node().kind() != "prim::Constant":
        return _unimplemented(name, "divisor_override")
    if not stride:
        stride = kernel_size
    padding = tuple(tuple_fn(padding))
    return padding
