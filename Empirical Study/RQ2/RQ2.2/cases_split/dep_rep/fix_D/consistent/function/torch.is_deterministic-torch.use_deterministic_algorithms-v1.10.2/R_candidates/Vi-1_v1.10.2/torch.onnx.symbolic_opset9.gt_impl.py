def gt_impl(g, input, other):
    if input.type().scalarType() is not None and input.type().scalarType() == "Bool" and \
            other.type().scalarType() is not None and other.type().scalarType() == "Bool":
        input = g.op("Cast", input, to_i=sym_help.cast_pytorch_to_onnx["Int"])
        other = g.op("Cast", other, to_i=sym_help.cast_pytorch_to_onnx["Int"])
    return g.op("Greater", input, other)
