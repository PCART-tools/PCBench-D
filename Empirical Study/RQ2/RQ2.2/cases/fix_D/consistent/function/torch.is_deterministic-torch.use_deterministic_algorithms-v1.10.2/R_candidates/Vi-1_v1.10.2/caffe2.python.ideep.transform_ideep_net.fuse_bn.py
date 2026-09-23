def fuse_bn(net, params, ignore_failure):
    # Run until we hit a fixed point
    removed_tensors = []
    while True:
        (next_net, next_params, removed_tensors) = \
            fuse_first_bn(net, params, removed_tensors)
        if len(next_net.op) == len(net.op):
            if (
                any(op.type == "SpatialBN" for op in next_net.op) and
                not ignore_failure
            ):
                raise Exception(
                    "Model contains SpatialBN op after fusion: %s", next_net)
            return (next_net, next_params, removed_tensors)
        net, params, removed_tensors = (next_net, next_params, removed_tensors)
