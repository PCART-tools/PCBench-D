@_onnx_symbolic("aten::aminmax")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "v", "i")
def aminmax(g: jit_utils.GraphContext, self, dim, keepdim):
    reduce_kwargs = {"keepdims_i": keepdim}
    if not symbolic_helper._is_none(dim):
        dim = symbolic_helper._get_const(dim, "i", "dim")
        reduce_kwargs["axes_i"] = [dim]

    return g.op("ReduceMin", self, **reduce_kwargs), g.op(
        "ReduceMax", self, **reduce_kwargs
    )
