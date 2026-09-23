@parse_args("v", "i", "i", "i")
def unsafe_chunk(g, self, chunks, dim, _outputs=None):
    if _outputs is None:
        return sym_help._onnx_opset_unsupported_detailed("unsafe_chunk", 9, 11, "Dynamic number of outputs not supported")
    size = sym_help._get_tensor_dim_size(self, dim)
    if size is None:
        return _unimplemented("unsafe_chunk", "unknown dimension size")
    split_size = (size + chunks - 1) // chunks
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    return g.op("Split", self, split_i=splits, axis_i=dim, outputs=_outputs)
