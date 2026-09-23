def defake(x):
    if not isinstance(x, FakeTensor):
        return x
    size: torch._prims_common.ShapeType
    stride: torch._prims_common.StrideType
    if x._has_symbolic_sizes_strides:
        size = []
        for s in x.size():
            if isinstance(s, torch.SymInt):
                size.append(s.node.shape_env.size_hint(s.node.expr))
            else:
                size.append(s)
        stride = []
        for s in x.stride():
            if isinstance(s, torch.SymInt):
                stride.append(s.node.shape_env.size_hint(s.node.expr))
            else:
                stride.append(s)
    else:
        size = x.size()
        stride = x.stride()
    y = torch.empty_strided(
        size,
        stride,
        dtype=x.dtype,
        device=x.device,
        requires_grad=x.requires_grad,
    )
    y.zero_()
    return y
