def eye(g, *args):
    if len(args) == 5:
        # aten::eye(n, dtype, layout, device, pin_memory)
        n, dtype, layout, device, pin_memory = args
        dim_size = sym_help._unsqueeze_helper(g, n, [0])
        shape = g.op("Concat", dim_size, dim_size, axis_i=0)
        tensor = zeros(g, shape, dtype, layout, device)
        return g.op("EyeLike", tensor)
    elif len(args) == 6:
        # aten::eye(n, m, dtype, layout, device, pin_memory)
        n, m, dtype, layout, device, pin_memory = args
        shape = g.op("Concat", sym_help._unsqueeze_helper(g, n, [0]), sym_help._unsqueeze_helper(g, m, [0]), axis_i=0)
        tensor = zeros(g, shape, dtype, layout, device)
        return g.op("EyeLike", tensor)
    else:
        raise NotImplementedError("Unknown aten::eye signature")
