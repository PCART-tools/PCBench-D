@parse_args("v", "i", "i", "none")
def sort(g, self, dim, decending, out=None):
    if out is not None:
        _unimplemented("Sort", "Out parameter is not supported for sort")
    self_sizes = sym_help._get_tensor_sizes(self)
    try:
        dim_size = self_sizes[dim]
    except Exception:
        dim_size = None

    if dim_size is None:
        return _unimplemented("Sort", "input size not accessible")

    return g.op("TopK", self, k_i=dim_size, axis_i=dim, outputs=2)
