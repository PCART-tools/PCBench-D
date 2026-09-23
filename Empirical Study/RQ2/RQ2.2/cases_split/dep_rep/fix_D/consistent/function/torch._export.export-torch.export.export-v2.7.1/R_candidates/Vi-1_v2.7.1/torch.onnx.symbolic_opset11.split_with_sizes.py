@_onnx_symbolic("aten::split_with_sizes")
@symbolic_helper.parse_args("v", "v", "i", "i")
def split_with_sizes(g: jit_utils.GraphContext, self, split_sizes, dim, _outputs=None):
    return split(g, self, split_sizes, dim, _outputs)
