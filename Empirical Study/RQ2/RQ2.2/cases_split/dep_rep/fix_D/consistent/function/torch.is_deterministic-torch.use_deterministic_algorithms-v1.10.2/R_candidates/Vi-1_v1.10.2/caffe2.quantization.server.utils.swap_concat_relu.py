def swap_concat_relu(net, ignore_op_with_output=None):
    # Run until we hit a fixed point
    while True:
        next_net = swap_first_concat_relu(net, ignore_op_with_output)
        if len(next_net.op) == len(net.op):
            return next_net
        net = next_net
