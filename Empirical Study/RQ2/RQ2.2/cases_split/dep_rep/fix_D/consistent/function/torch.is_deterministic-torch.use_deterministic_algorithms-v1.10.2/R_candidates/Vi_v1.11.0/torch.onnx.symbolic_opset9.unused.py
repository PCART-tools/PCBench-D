def unused(g):
    n = g.op("prim::Constant")
    n.setType(OptionalType.ofTensor())
    return n
