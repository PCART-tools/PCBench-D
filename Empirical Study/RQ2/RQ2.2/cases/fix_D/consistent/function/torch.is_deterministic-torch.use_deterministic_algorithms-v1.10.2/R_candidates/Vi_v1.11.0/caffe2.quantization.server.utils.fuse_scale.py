def fuse_scale(net, params, ignore_failure):
    # Run until we hit a fixed point
    removed_tensors = []
    while True:
        (next_net, next_params, removed_tensors) = fuse_first_scale(
            net, params, removed_tensors
        )
        if len(next_net.op) == len(net.op):
            return (next_net, next_params, removed_tensors)
        net, params, removed_tensors = (next_net, next_params, removed_tensors)
