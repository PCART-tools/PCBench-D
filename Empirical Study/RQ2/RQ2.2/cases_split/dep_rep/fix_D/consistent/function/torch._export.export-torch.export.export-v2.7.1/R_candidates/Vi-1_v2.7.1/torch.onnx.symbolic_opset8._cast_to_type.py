def _cast_to_type(g: jit_utils.GraphContext, input, to_type):
    if to_type is None:
        return input
    return getattr(opset9, f"_cast_{to_type}")(g, input, False)
