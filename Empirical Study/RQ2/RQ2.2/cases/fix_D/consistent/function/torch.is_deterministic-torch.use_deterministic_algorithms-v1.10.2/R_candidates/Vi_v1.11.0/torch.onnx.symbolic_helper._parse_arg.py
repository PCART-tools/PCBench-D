def _parse_arg(value, desc, arg_name=None, node_name=None):
    if desc == "none":
        return value
    if desc == "v" or not _is_value(value):
        return value
    if value.node().mustBeNone():
        return None
    if value.node().kind() == "onnx::Constant":
        tval = value.node()["value"]
        if desc == "i":
            return int(tval)
        elif desc == "f":
            return float(tval)
        elif desc == "b":
            return bool(tval)
        elif desc == "s":
            return str(tval)
        elif desc == "t":
            return tval
        elif desc == "is":
            return [int(v) for v in tval]
        elif desc == "fs":
            return [float(v) for v in tval]
        else:
            raise RuntimeError("ONNX symbolic doesn't know to interpret Constant node")
    elif value.node().kind() == "prim::ListConstruct":
        if desc == "is":
            for v in value.node().inputs():
                if v.node().kind() != "onnx::Constant":
                    raise RuntimeError("Failed to export an ONNX attribute '" + v.node().kind() +
                                       "', since it's not constant, please try to make "
                                       "things (e.g., kernel size) static if possible")
            return [int(v.node()["value"]) for v in value.node().inputs()]
        else:
            raise RuntimeError("ONNX symbolic doesn't know to interpret ListConstruct node")

    if arg_name is None or node_name is None:
        raise RuntimeError("Expected node type 'onnx::Constant', got '{}'.".format(value.node().kind()))
    else:
        raise RuntimeError("Expected node type 'onnx::Constant' "
                           "for argument '{}' of node '{}', got '{}'.".format(arg_name, node_name, value.node().kind()))
