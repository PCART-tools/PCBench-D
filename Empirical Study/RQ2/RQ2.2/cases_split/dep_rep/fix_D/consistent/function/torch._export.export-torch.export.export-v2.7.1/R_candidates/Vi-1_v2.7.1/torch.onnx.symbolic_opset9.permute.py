@_onnx_symbolic("aten::permute")
@symbolic_helper.parse_args("v", "is")
def permute(g: jit_utils.GraphContext, self, dims):
    if dims == list(range(0, len(dims))):
        return self
    return g.op("Transpose", self, perm_i=dims)
