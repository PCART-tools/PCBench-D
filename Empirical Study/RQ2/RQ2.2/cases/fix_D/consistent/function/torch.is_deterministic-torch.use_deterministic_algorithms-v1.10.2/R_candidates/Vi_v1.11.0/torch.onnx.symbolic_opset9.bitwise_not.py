def bitwise_not(g, inp):
    if inp.type().scalarType() != "Bool":
        raise NotImplementedError("ONNX export does NOT support exporting bitwise Not " +
                                  "for non-boolean input values")
    return g.op("Not", inp)
