def fuse_first_bn(net, params, removed_tensors, begin_op_index):
    net = copy.deepcopy(net)
    params = copy.deepcopy(params)

    for i, conv in enumerate(net.op[begin_op_index:], begin_op_index):
        if conv.type not in ["Conv", "ConvTranspose"]:
            continue

        uses = blob_uses(net, conv.output[0])
        if len(uses) == 0:
            continue

        j = uses[0]
        bn = net.op[j]
        if bn.type != "SpatialBN" or (len(uses) > 1 and conv.output[0] != bn.output[0]):
            if bn.type == "SpatialBN":
                logger.debug("Can't fuse if more than one user {}".format(uses))
            # Can't fuse if more than one user unless SpatialBN is inplace
            # An example of inplace SpatialBN where we want to allow multiple uses:
            # x = Conv(...)
            # ... // no interferring use or def of x (will be checked below)
            # x = SpatialBN(x, ...)
            # ...
            # z = Foo(..., x, ...)
            # ...
            # w = Boo(..., x, ...)
            # Here, we still want to fuse Conv and SpatialBN
            continue

        # There shouldn't be any def of conv.output[0] and any use or def of bn.output[0] between conv and bn
        if any(
            blob in net.op[k].input or blob in net.op[k].output
            for blob in [conv.output[0], bn.output[0]]
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
        fused_conv.output[0] = bn.output[0]
        conv_weight = params[conv.input[1]]
        if len(conv.input) > 2:
            conv_bias = params[conv.input[2]]
        else:
            conv_bias = np.zeros(len(params[bn.input[2]])).astype(np.float32)

        bn_scale = params[bn.input[1]]
        bn_bias = params[bn.input[2]]
        bn_running_mean = params[bn.input[3]]
        bn_running_var = params[bn.input[4]]

        # First, BN computation can be phrased as follows:
        # (X - running_mean) * (1.0 / sqrt(running_var + eps)) *
        # bn_scale + bias
        # Thus, we can rewrite bn_scale as:
        # X * bn_scale * 1.0 / (sqrt(running_var + eps)) + (bias -
        # running_mean * (1.0 / sqrt(running_var + eps)) * bn_scale)
        # Thus, can just have the affine transform
        # X * A + B
        # where
        # A = bn_scale * 1.0 / (sqrt(running_var + eps))
        # B =  (bias - running_mean * (1.0 / sqrt(running_var + eps))
        # * bn_scale)
        eps = 1.0e-5
        for arg in bn.arg:
            if arg.name == "epsilon":
                eps = arg.f
        A = bn_scale * 1.0 / (np.sqrt(bn_running_var + eps))
        B = bn_bias - bn_running_mean * A

        # This identity should hold if we have correctly fused
        # np.testing.assert_array_equal(
        #     params[conv.output[0]] * A + B,
        #     params[bn.output[0]])

        # Now, we have that the computation made is the following:
        # ((X `conv` W) + b) * A + B
        # Then, we can simply fuse this as follows:
        # (X `conv` (W * A)) + b * A + B
        # which is simply
        # (X `conv` Q) + C
        # where

        # Q = W * A
        # C = b * A + B

        # For ConvTranspose, from the view of convolutions as a
        # Toepeliz multiplication, we have W_ = W^T, so the weights
        # are laid out as (R, S, K, K) (vs (S, R, K, K) for a Conv),
        # so the weights broadcast slightly differently. Remember, our
        # BN scale 'B' is of size (S,)

        A_ = (
            A.reshape((-1,) + tuple([1] * (conv_weight.ndim - 1)))
            if conv.type == "Conv"
            else A.reshape((1, -1) + tuple([1] * (conv_weight.ndim - 2)))
        )

        C = conv_bias * A + B
        Q = conv_weight * A_

        assert params[conv.input[1]].shape == Q.shape
        if len(conv.input) > 2:
            assert params[conv.input[2]].shape == C.shape
        else:
            assert bn_bias.shape == C.shape

        params[conv.input[1]] = Q
        if len(conv.input) > 2:
            params[conv.input[2]] = C
        else:
            params[bn.input[2]] = C
            fused_conv.input.append(bn.input[2])

        new_ops = net.op[:i] + [fused_conv] + net.op[i + 1 : j] + net.op[j + 1 :]
        del net.op[:]
        removed_tensors.append(bn.input[1])
        if len(conv.input) > 2:
            removed_tensors.append(bn.input[2])
        removed_tensors.append(bn.input[3])
        removed_tensors.append(bn.input[4])
        del params[bn.input[1]]
        if len(conv.input) > 2:
            del params[bn.input[2]]
        del params[bn.input[3]]
        del params[bn.input[4]]
        net.op.extend(new_ops)
        return net, params, removed_tensors, i + 1

    return net, params, removed_tensors, None
