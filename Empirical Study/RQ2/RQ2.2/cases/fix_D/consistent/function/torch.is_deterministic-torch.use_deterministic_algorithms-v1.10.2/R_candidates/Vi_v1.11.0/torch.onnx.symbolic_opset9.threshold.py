@parse_args("v", "t", "t")
def threshold(g, self, threshold, value):
    # See Note [Export inplace]
    if sym_help._scalar(threshold) != 0:
        return _unimplemented("threshold", "non-zero threshold")
    if sym_help._scalar(value) != 0:
        return _unimplemented("threshold", "non-zero value")
    return g.op("Relu", self)
