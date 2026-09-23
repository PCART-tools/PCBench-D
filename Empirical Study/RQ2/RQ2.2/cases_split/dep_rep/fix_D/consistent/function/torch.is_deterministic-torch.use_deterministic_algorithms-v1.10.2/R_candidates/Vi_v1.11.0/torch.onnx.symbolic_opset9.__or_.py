def __or_(g, input, other):
    if input.type().scalarType() == "Bool" and \
            other.type().scalarType() == "Bool":
        return g.op("Or", input, other)
    else:
        raise NotImplementedError("ONNX export does NOT support exporting bitwise OR " +
                                  "for non-boolean input values")
