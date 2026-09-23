def unused(g):
    """Represents "missing" optional inputs."""
    n = g.op("prim::Constant")
    n.setType(_C.OptionalType.ofTensor())
    return n
