def convertAttributeProto(onnx_arg):
    """
    Convert an ONNX AttributeProto into an appropriate Python object
    for the type.

    NB: Tensor attribute gets returned as the straight proto.
    """
    if onnx_arg.HasField('f'):
        return onnx_arg.f
    elif onnx_arg.HasField('i'):
        return onnx_arg.i
    elif onnx_arg.HasField('s'):
        return onnx_arg.s
    elif onnx_arg.HasField('t'):
        return onnx_arg.t  # this is a proto!
    elif onnx_arg.HasField('g'):
        return Caffe2Backend._graph_to_net(onnx_arg.g, Caffe2Backend._known_opset_version)
    elif len(onnx_arg.floats):
        return list(onnx_arg.floats)
    elif len(onnx_arg.ints):
        return list(onnx_arg.ints)
    elif len(onnx_arg.strings):
        return list(onnx_arg.strings)
    elif len(onnx_arg.graphs):
        retval = []
        # TODO: this doesn't work with RNN ops
        for g in onnx_arg.graphs:
            retval.append(Caffe2Backend._graph_to_net(g, Caffe2Backend._known_opset_version))
        return retval
    else:
        raise ValueError("Unsupported ONNX attribute: {}".format(onnx_arg))
