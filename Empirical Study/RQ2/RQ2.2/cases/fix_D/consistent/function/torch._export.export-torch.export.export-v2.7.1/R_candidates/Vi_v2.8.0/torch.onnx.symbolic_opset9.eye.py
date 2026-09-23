@_onnx_symbolic("aten::eye")
def eye(g: jit_utils.GraphContext, *args):
    if len(args) == 5:
        # aten::eye(n, dtype, layout, device, pin_memory)
        n, dtype, layout, device, _pin_memory = args
        dim_size = symbolic_helper._unsqueeze_helper(g, n, [0])
        shape = g.op("Concat", dim_size, dim_size, axis_i=0)
        tensor = zeros(g, shape, dtype, layout, device)
        return g.op("EyeLike", tensor)
    if len(args) == 6:
        # aten::eye(n, m, dtype, layout, device, pin_memory)
        n, m, dtype, layout, device, _pin_memory = args
        shape = g.op(
            "Concat",
            symbolic_helper._unsqueeze_helper(g, n, [0]),
            symbolic_helper._unsqueeze_helper(g, m, [0]),
            axis_i=0,
        )
        tensor = zeros(g, shape, dtype, layout, device)
        return g.op("EyeLike", tensor)

    return symbolic_helper._unimplemented("aten::eye", f"with {len(args)} arguments")
