@_onnx_symbolic("aten::frobenius_norm")
@symbolic_helper.parse_args("v", "v", "i")
def frobenius_norm(g: jit_utils.GraphContext, self, dim=None, keepdim=False):
    dim_val = symbolic_helper._maybe_get_const(dim, "is")
    if not symbolic_helper._is_value(dim_val) and len(dim_val) == 0:
        return g.op("ReduceL2", self, keepdims_i=0)
    sqr = g.op("Mul", self, self)
    sumsqr = symbolic_helper._reducesum_helper(g, sqr, dim, keepdims_i=keepdim)
    return g.op("Sqrt", sumsqr)
