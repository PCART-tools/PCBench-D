def _cast_to_type(g, input, to_type):
    if to_type is None:
        return input
    return getattr(sym_opset9, "_cast_{}".format(to_type))(g, input, False)
