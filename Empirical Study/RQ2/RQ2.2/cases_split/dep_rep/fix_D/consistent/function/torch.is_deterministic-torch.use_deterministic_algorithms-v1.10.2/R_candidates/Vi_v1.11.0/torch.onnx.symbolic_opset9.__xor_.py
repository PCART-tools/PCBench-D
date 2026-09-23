def __xor_(g, input, other):
    if input.type().scalarType() == "Bool" and \
            other.type().scalarType() == "Bool":
        return g.op("Xor", input, other)
    else:
        raise NotImplementedError("ONNX export does NOT support exporting bitwise XOR " +
                                  "for non-boolean input values")
