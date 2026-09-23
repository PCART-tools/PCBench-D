def fuse_first_bn(net, params, removed_tensors):
    net = copy.deepcopy(net)
    params = copy.deepcopy(params)

    for ((i, current), (j, next_)) in pairwise(enumerate(net.op)):
        if next_.input[0] != current.output[0]:
            continue

        if current.type not in ("Conv", "ConvTranspose") \
           or next_.type != "SpatialBN":
            continue
        if len(blob_uses(net, current.output[0])) != 1:
            # Can't fuse if more than one user
            continue

        # else, can fuse
        conv = current
        bn = next_
        fused_conv = copy.deepcopy(conv)
        fused_conv.output[0] = bn.output[0]

        # Fix fused_conv to ensure we have a bias passed.
        if len(fused_conv.input) != 3:
            bias_name = "{}_bias".format(conv.input[1])
            net.external_input.extend([bias_name])
            fused_conv.input.extend([bias_name])
            for arg in fused_conv.arg:
                if arg.name == "no_bias":
                    arg.i = 0

        conv_weight = params[conv.input[1]]
        conv_bias = params[conv.input[2]] if len(conv.input) == 3 \
            else np.zeros(shape=(conv_weight.shape[0])).astype(np.float32)

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

        # This identify should hold if we have correctly fused
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

        A_ = A.reshape(-1, 1, 1, 1) if conv.type == "Conv" else \
            A.reshape(1, -1, 1, 1)

        C = conv_bias * A + B
        Q = conv_weight * A_

        params[fused_conv.input[1]] = Q
        params[fused_conv.input[2]] = C
        new_ops = net.op[:i] + [fused_conv] + net.op[j + 1:]
        del net.op[:]
        removed_tensors.append(bn.input[1])
        removed_tensors.append(bn.input[2])
        removed_tensors.append(bn.input[3])
        removed_tensors.append(bn.input[4])
        del params[bn.input[1]]
        del params[bn.input[2]]
        del params[bn.input[3]]
        del params[bn.input[4]]
        net.op.extend(new_ops)
        break
    return net, params, removed_tensors
