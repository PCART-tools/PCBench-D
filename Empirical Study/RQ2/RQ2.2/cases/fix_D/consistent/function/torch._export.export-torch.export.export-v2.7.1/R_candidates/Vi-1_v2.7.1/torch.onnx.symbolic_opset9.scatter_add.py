@_onnx_symbolic("aten::scatter_add")
@symbolic_helper.parse_args("v", "i", "v", "v")
def scatter_add(g: jit_utils.GraphContext, self, dim, index, src):
    scalar_type = symbolic_helper._try_get_scalar_type(self)
    if scalar_type is None:
        return symbolic_helper._unimplemented(
            "scatter_add", "input dtype not accessible", self
        )
    sizes = symbolic_helper._get_tensor_sizes(self, allow_nonstatic=False)
    if sizes:
        to_add = g.op("Constant", value_t=torch.zeros(sizes, dtype=scalar_type.dtype()))
    else:
        to_add = zeros_like(g, self, scalar_type)
    to_add = symbolic_helper._scatter_helper(g, to_add, dim, index, src)
    return add(g, self, to_add)
