@parse_args("v", "v", "v", "i")
def split(g, self, split_size_or_sizes, dim, _outputs=None):
    if not sym_help._is_split_static(split_size_or_sizes, _outputs):
        return sym_help._onnx_opset_unsupported_detailed("split", 9, 11, "Dynamic number of outputs not supported")
    split_val = split_size_or_sizes.node()["value"]
    if split_val.dim() > 0:
        return split_with_sizes(g, self, split_size_or_sizes, dim, _outputs)
    split_size = sym_help._get_const(split_size_or_sizes, "i", "split_size")
    dim = sym_help._get_const(dim, "i", "dim")

    size = sym_help._get_tensor_dim_size(self, dim)
    if size is None:
        if _outputs is not None:
            size = split_size * _outputs
        else:
            return sym_help._onnx_opset_unsupported_detailed("split", 9, 11, "Unknown dimension size not supported")
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    return g.op("Split", self, split_i=splits, axis_i=dim, outputs=_outputs)
