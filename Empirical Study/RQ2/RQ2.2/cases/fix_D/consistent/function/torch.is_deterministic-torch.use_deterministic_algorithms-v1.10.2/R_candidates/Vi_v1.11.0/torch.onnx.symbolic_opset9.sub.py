def sub(g, self, other, alpha=None):
    # default alpha arg is to allow no-alpha sub (aten sub st overload no alpha)
    if alpha and sym_help._scalar(sym_help._maybe_get_scalar(alpha)) != 1:
        return _unimplemented("sub", "alpha != 1")
    return g.op("Sub", self, other)
