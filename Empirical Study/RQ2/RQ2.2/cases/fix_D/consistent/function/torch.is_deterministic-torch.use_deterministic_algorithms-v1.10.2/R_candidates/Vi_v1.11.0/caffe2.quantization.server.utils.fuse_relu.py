def fuse_relu(net, ignore_failure, ignore_op_with_output=None):
    # Run until we hit a fixed point
    begin_op_index = 0
    while True:
        next_net, begin_op_index = fuse_first_relu(
            net, begin_op_index, ignore_op_with_output
        )
        if begin_op_index is None:
            if any(op.type == "Relu" for op in next_net.op) and not ignore_failure:
                raise Exception("Model contains Relu op after fusion: %s", next_net)
            return next_net
        net = next_net
