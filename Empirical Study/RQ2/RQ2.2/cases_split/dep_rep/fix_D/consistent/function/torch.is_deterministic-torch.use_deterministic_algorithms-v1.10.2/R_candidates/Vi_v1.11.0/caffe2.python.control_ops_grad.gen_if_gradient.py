def gen_if_gradient(op, g_output):
    """
    Generates gradient If operator, given forward If op and a list
    of gradient blobs corresponding to forward op's outputs
    Returns a gradient op and a list of blobs corresponding to input gradients
    """
    from caffe2.python.core import BlobReference
    assert op.type == "If", "Expected If op"
    # first input is the condition blob
    assert len(op.input) > 0, "Expected at least one input in If op"

    assert len(op.output) == len(g_output), \
        "Different number of gradient blobs and If op outputs"

    grad_ops, deduped_g_output = dedupe_g_output(op, g_output)
    g_output = deduped_g_output

    init_grad_map = {}  # map from if's output blob to output gradient blob
    op_input = [str(i) for i in op.input]
    op_output = [str(o) for o in op.output]
    for output_name, grad_output_name in zip(op_output, g_output):
        if grad_output_name:
            init_grad_map[BlobReference(output_name)] = \
                BlobReference(grad_output_name)
    # shouldn't call without at least one output gradient available
    assert len(init_grad_map) > 0, "Empty initial gradient map for If op"

    grad_map = {}  # map from blob to gradient blob
    then_net = _get_net_argument(op, "then_net")
    assert then_net, "Expected then subnet in If op"
    then_grad_net, then_grad_map, then_input_names, then_output_names = \
        _gen_subnet_gradient(then_net, init_grad_map)
    assert then_grad_net, "Failed to get gradient net for then in If op"
    grad_map.update(then_grad_map)

    else_input_names = set()
    else_output_names = set()
    else_grad_map = {}
    else_grad_net = None
    else_net = _get_net_argument(op, "else_net")
    if else_net:
        else_grad_net, else_grad_map, else_input_names, else_output_names = \
            _gen_subnet_gradient(else_net, init_grad_map)
        assert else_grad_net, "Failed to get gradient net for else in If op"
        # consider case: else doesn't update blob's gradient and keeps original
        # from init_grad_map, but then updates the gradient
        for else_blob, else_grad_blob in else_grad_map.items():
            if else_blob in then_grad_map:
                then_grad_blob = then_grad_map[else_blob]
                # if both then and else branches have grad blob name for the same
                # blob and grad names are different, then one of the branches
                # doesn't use blob and has original grad blob name in it's grad map,
                # and another branch uses blob and has <blob_name>_grad name
                # in it's grad map (might be different from original grad blob)
                if then_grad_blob != else_grad_blob:
                    init_grad_name = init_grad_map[else_blob] \
                        if else_blob in init_grad_map else None

                    if then_grad_blob == init_grad_name:
                        grad_map[else_blob] = else_grad_blob
                    elif else_grad_blob == init_grad_name:
                        grad_map[else_blob] = then_grad_blob
                    else:
                        raise "Unexpected grad blob name " + else_blob + ", " + \
                            else_grad_blob + ", " + then_grad_blob
            else:
                grad_map[else_blob] = else_grad_blob

    # make sure gradients of blobs that were not computed
    # by the selected if's branch are initialized with zeros
    then_other_output_names = \
        then_output_names - (then_output_names & else_output_names)
    then_other_grad_output_names = set(
        [o for o in then_other_output_names if o in then_grad_map.values()])
    zero_then = _gen_grad_zero_init_ops(
        init_grad_map, then_grad_map, then_other_grad_output_names)
    if else_grad_net:
        else_grad_net.op.extend(zero_then)
    elif len(zero_then) > 0:
        else_grad_net = caffe2_pb2.NetDef()
        else_grad_net.CopyFrom(then_grad_net)
        if else_grad_net.name:
            else_grad_net.name += "_auto_else_zero_blobs_"
        del else_grad_net.op[:]
        else_grad_net.op.extend(zero_then)
        del else_grad_net.external_input[:]
        del else_grad_net.external_output[:]

    else_other_output_names = \
        else_output_names - (then_output_names & else_output_names)
    else_other_grad_output_names = set(
        [o for o in else_other_output_names if o in else_grad_map.values()])
    zero_else = _gen_grad_zero_init_ops(
        init_grad_map, else_grad_map, else_other_grad_output_names)
    then_grad_net.op.extend(zero_else)

    output_names = list(then_output_names | else_output_names)
    input_names = then_input_names | else_input_names
    # make sure condition blob is the first in the list
    input_names = [op_input[0]] + list(input_names - set(op_input[0]))
    gradient_if_def = _prepare_gradient_if_op(
        fwd_op=op,
        input_names=input_names,
        output_names=output_names,
        then_grad_net=then_grad_net,
        else_grad_net=else_grad_net)
    g_input = [grad_map.get(i, None) for i in op_input]
    return grad_ops + [gradient_if_def], g_input
