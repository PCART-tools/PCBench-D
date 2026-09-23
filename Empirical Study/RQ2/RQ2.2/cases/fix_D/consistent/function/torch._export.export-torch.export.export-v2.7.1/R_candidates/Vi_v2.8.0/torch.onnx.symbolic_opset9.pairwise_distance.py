@_onnx_symbolic("aten::pairwise_distance")
def pairwise_distance(g: jit_utils.GraphContext, input1, input2, p, eps, keepdim):
    if not symbolic_helper._is_value(eps):
        eps = g.op("Constant", value_t=torch.tensor([eps]))
    inv_p = div(
        g,
        g.op("Constant", value_t=torch.tensor([1], dtype=torch.float)),
        add(g, p, eps),
    )
    summation = symbolic_helper._reducesum_helper(
        g,
        pow(g, sub(g, input1, input2), p),
        axes_i=[-1],
        keepdims_i=symbolic_helper._parse_arg(keepdim, "i"),
    )
    return pow(g, summation, inv_p)
