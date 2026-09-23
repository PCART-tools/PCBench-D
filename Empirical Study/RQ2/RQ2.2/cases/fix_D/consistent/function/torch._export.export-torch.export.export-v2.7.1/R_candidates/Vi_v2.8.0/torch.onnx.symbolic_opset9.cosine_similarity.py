@_onnx_symbolic("aten::cosine_similarity")
@symbolic_helper.parse_args("v", "v", "i", "f")
def cosine_similarity(g: jit_utils.GraphContext, x1, x2, dim, eps):
    cross = symbolic_helper._reducesum_helper(
        g, mul(g, x1, x2), axes_i=[dim], keepdims_i=0
    )
    x1_l2 = symbolic_helper._reducesum_helper(
        g, mul(g, x1, x1), axes_i=[dim], keepdims_i=0
    )
    x2_l2 = symbolic_helper._reducesum_helper(
        g, mul(g, x2, x2), axes_i=[dim], keepdims_i=0
    )
    div_tens = max(
        g, sqrt(g, mul(g, x1_l2, x2_l2)), g.op("Constant", value_t=torch.tensor([eps]))
    )
    return div(g, cross, div_tens)
