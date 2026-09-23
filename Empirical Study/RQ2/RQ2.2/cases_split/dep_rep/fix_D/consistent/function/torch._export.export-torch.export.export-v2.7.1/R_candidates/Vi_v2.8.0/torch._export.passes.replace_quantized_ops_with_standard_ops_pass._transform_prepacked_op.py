def _transform_prepacked_op(gm: torch.fx.GraphModule, node: torch.fx.Node):
    """
    Transformation for functions under prepacked namespace, where they share
    the same handling logic that [...]OpContext contains all parameters.
    """
    assert isinstance(node.target, torch._ops.OpOverload)
    opname, args = node.target._opname, node.args
    op_f = None
    if opname == "conv2d_clamp_run":
        op_f = torch.ops.aten.conv2d
    elif opname == "linear_clamp_run":
        op_f = torch.ops.aten.linear
    else:
        raise RuntimeError(f"Invalid operator {opname}")

    assert isinstance(args[1], torch.fx.Node)
    so = get_script_object(gm, args[1])

    func_args = []
    func_args += [args[0]]
    func_args += so.unpack()[:2]  # type: ignore[attr-defined]
    if opname == "conv2d_clamp_run":
        func_args += torch.ops.prepacked.unpack_prepacked_sizes_conv2d(so)[2:]

    op_res_node = gm.graph.call_function(op_f, tuple(func_args))
    return op_res_node
