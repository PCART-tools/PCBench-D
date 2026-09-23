def __not_(g, self):
    if self.type().scalarType() != "Bool":
        raise NotImplementedError("ONNX export does NOT support exporting bitwise Not " +
                                  "for non-boolean input values")
    return g.op("Not", self)
