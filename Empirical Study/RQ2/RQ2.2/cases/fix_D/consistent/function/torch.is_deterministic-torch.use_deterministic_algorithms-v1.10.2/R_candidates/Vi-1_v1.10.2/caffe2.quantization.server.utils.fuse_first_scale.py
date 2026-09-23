def fuse_first_scale(net, params, removed_tensors):
    net = copy.deepcopy(net)
    params = copy.deepcopy(params)

    for ((i, current), (j, next_)) in pairwise(enumerate(net.op)):
        if next_.input[0] != current.output[0]:
            continue

        if (
            current.type != "SpatialBN"
            or next_.type != "Mul"
            or len(net.op) <= j + 1
            or net.op[j + 1].type != "Add"
        ):
            continue

        # else, can fuse
        bn = current
        mul = next_
        add = net.op[j + 1]

        fused_bn = copy.deepcopy(bn)
        fused_bn.output[0] = add.output[0]
        bn_scale = params[bn.input[1]]
        mul_scale = params[mul.input[1]]
        bn_bias = params[bn.input[2]]
        add_bias = params[add.input[1]]

        params[bn.input[1]] = bn_scale * mul_scale
        params[bn.input[2]] = mul_scale * bn_bias + add_bias

        new_ops = net.op[:i] + [fused_bn] + net.op[j + 2 :]
        del net.op[:]
        removed_tensors.append(mul.input[1])
        removed_tensors.append(add.input[1])
        del params[mul.input[1]]
        del params[add.input[1]]
        net.op.extend(new_ops)
        break
    return net, params, removed_tensors
