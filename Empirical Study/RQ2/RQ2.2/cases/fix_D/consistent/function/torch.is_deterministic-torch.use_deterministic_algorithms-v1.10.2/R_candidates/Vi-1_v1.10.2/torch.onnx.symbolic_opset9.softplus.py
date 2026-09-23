@parse_args("v", "t", "v")
def softplus(g, self, beta, threshold):
    if beta != 1:
        return _unimplemented("beta", "has to be 1")
    return g.op("Softplus", self)
