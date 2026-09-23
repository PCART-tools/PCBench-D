def gen_while_gradient(op, g_output):
    """
    Generates gradient While operator
    """
    from caffe2.python.core import BlobReference
    assert op.type == "While", "Expected While op"
    assert len(op.input) > 0, "Expected at least one input in While op"

    assert len(op.output) == len(g_output), \
        "Different number of gradient blobs and While op outputs"

    grad_ops, deduped_g_output = dedupe_g_output(op, g_output)
    g_output = deduped_g_output

    init_grad_map = {}
    op_output = [str(o) for o in op.output]
    for output_name, grad_output_name in zip(op_output, g_output):
        if grad_output_name:
            init_grad_map[BlobReference(output_name)] = \
                BlobReference(grad_output_name)
    assert len(init_grad_map) > 0, "Empty initial gradient map for While op"

    loop_net = _get_net_argument(op, "loop_net")
    assert loop_net, "Expected loop subnet in While op"
    assert len(loop_net.op) == 1 and loop_net.op[0].type == "Do", \
        "Gradient While op requires single Do op as a loop body"
    do_op = loop_net.op[0]
    do_args = _get_do_arguments(do_op)
    assert "reuse_workspace" not in do_args or not do_args["reuse_workspace"], \
        "Gradient While op requires Do loop body op without reuse_workspace set"

    assert len(do_op.output) > 0, "Expected Do op with at least one output"
    workspace_blob = do_op.output[-1]

    loop_grad_net, loop_grad_map, loop_input_names, loop_output_names = \
        _gen_subnet_gradient(loop_net, init_grad_map)
    assert loop_grad_net, "Failed to get gradient net for loop body in While op"

    grad_ops += _prepare_gradient_while_ops(
        fwd_op=op,
        input_names=loop_input_names,
        output_names=loop_output_names,
        loop_grad_net=loop_grad_net,
        workspace_blob=workspace_blob,
        init_grad_map=init_grad_map,
        loop_grad_map=loop_grad_map)

    op_input = [str(i) for i in op.input]
    g_input = [loop_grad_map.get(i, None) for i in op_input]
    return grad_ops, g_input
