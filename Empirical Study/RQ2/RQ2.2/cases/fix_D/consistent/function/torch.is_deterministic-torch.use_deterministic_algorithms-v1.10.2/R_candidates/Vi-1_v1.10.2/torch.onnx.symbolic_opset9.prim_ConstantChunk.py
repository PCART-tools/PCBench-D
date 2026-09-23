def prim_ConstantChunk(g, self, chunks, dim):
    dim_size = sym_help._get_tensor_dim_size(self, dim)
    if dim_size is None:
        return _unimplemented("prim::ConstantChunk", "unknown dimension size")
    split_size = (dim_size + chunks - 1) // chunks
    return prim_ConstantSplit(g, self, split_size, dim)
