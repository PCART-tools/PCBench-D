@_onnx_symbolic("prim::ConstantChunk")
def prim_constant_chunk(g: jit_utils.GraphContext, self, chunks, dim):
    dim_size = symbolic_helper._get_tensor_dim_size(self, dim)
    if dim_size is None:
        return symbolic_helper._unimplemented(
            "prim::ConstantChunk", "unknown dimension size", self
        )
    split_size = (dim_size + chunks - 1) // chunks
    return prim_constant_split(g, self, split_size, dim)
