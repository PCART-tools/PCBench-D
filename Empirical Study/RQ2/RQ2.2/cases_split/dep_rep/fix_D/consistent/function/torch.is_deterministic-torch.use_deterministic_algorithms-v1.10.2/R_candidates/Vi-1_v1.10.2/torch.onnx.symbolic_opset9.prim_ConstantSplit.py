def prim_ConstantSplit(g, self, split_size, dim):
    size = sym_help._get_tensor_dim_size(self, dim)
    if size is None:
        return _unimplemented("prim::ConstantSplit", "unknown dimension size")
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    return g.op("Split", self, split_i=splits, axis_i=dim, outputs=len(splits))
