def fuse_first_relu(net, begin_op_index, ignore_op_with_output=None):
    net = copy.deepcopy(net)

    for i, conv in enumerate(net.op[begin_op_index:], begin_op_index):
        if conv.type not in ["Conv", "ConvTranspose", "Sum", "SpatialBN"]:
            continue

        uses = blob_uses(net, conv.output[0])
        if (
            len(uses) == 0
            or ignore_op_with_output
            and conv.output[0] in ignore_op_with_output
        ):
            continue

        j = uses[0]
        relu = net.op[j]
        if relu.type != "Relu" or len(uses) > 1 and conv.output[0] != relu.output[0]:
            # Can't fuse if more than one user unless Relu is inplace
            if relu.type == "Relu":
                logger.debug("Can't fuse if more than one user {}".format(uses))
            continue

        # There shouldn't be any def of conv.output[0] and any use or def of relu.output[0] between conv and relu
        if any(
            blob in net.op[k].input or blob in net.op[k].output
            for blob in [conv.output[0], relu.output[0]]
            for k in range(i + 1, j)
        ):
            logger.debug(
                "Can't fuse because of the following interferring uses or defs:"
            )
            for k in range(i, j + 1):
                logger.debug(net.op[k])
            continue

        # else, can fuse
        fused_conv = copy.deepcopy(conv)
        fused_conv.type = conv.type + "Relu"
        fused_conv.output[0] = relu.output[0]

        new_ops = net.op[:i] + [fused_conv] + net.op[i + 1 : j] + net.op[j + 1 :]
        del net.op[:]
        net.op.extend(new_ops)
        return net, i + 1
    return net, None
