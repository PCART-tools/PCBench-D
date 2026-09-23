def _get_const(value, desc, arg_name):
    if not _is_constant(value):
        raise RuntimeError("ONNX symbolic expected a constant value of the {} argument, got `{}`".format(arg_name, value))
    return _parse_arg(value, desc)
