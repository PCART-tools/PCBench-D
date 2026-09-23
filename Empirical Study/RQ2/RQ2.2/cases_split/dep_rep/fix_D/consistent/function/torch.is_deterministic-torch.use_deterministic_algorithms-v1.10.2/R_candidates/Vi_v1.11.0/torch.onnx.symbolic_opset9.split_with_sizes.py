@parse_args("v", "is", "i", "i")
def split_with_sizes(g, self, split_sizes, dim, _outputs=None):
    if not sym_help._is_split_static(split_sizes, _outputs):
        return sym_help._onnx_opset_unsupported_detailed("split_with_sizes", 9, 11, "Dynamic number of outputs not supported")
    return g.op("Split", self, split_i=split_sizes, axis_i=dim, outputs=_outputs)
