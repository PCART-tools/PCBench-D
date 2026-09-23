@_onnx_symbolic("aten::linspace")
def linspace(
    g: jit_utils.GraphContext, start, end, steps, dtype, layout, device, pin_memory
):
    range_tensor = symbolic_helper._arange_helper(g, steps, None)
    step = div(
        g,
        sub(g, end, start),
        sub(g, steps, g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))),
    )
    return add(g, mul(g, range_tensor, step), start)
