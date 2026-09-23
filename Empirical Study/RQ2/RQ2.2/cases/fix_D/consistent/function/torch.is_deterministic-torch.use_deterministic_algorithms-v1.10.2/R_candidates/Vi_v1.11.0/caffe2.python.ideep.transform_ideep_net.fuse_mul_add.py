def fuse_mul_add(net, params):
    # Run until we hit a fixed point
    removed_tensors = []
    while True:
        (next_net, next_params, removed_tensors) = \
            fuse_first_mul_add(net, params, removed_tensors)
        if len(next_net.op) == len(net.op):
            return (next_net, next_params, removed_tensors)
        net, params, removed_tensors = (next_net, next_params, removed_tensors)
