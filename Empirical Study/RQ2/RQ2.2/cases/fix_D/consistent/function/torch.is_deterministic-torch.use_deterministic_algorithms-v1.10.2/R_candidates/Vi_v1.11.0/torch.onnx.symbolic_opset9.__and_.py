def __and_(g, input, other):
    if input.type().scalarType() == "Bool" and \
            other.type().scalarType() == "Bool":
        return g.op("And", input, other)
    else:
        raise NotImplementedError("ONNX export does NOT support exporting bitwise AND " +
                                  "for non-boolean input values")
