def fuse_bn(net, params, ignore_failure):
    # Run until we hit a fixed point
    removed_tensors = []
    begin_op_index = 0
    while True:
        (next_net, next_params, removed_tensors, begin_op_index) = fuse_first_bn(
            net, params, removed_tensors, begin_op_index
        )
        if begin_op_index is None:
            if any(op.type == "SpatialBN" for op in next_net.op) and not ignore_failure:
                raise Exception(
                    "Model contains SpatialBN op after fusion: %s", next_net
                )
            return (next_net, next_params, removed_tensors)
        net, params, removed_tensors = (next_net, next_params, removed_tensors)
